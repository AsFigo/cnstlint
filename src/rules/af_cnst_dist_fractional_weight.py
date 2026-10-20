# ----------------------------------------------------
# SPDX-FileCopyrightText: AsFigo Technologies, UK
# SPDX-FileCopyrightText: VerifWorks, India
# SPDX-License-Identifier: MIT
# ----------------------------------------------------

from af_lint_rule import AsFigoLintRule


class CnstDistFractionalWeight(AsFigoLintRule):
    """
    **CNST_DIST_FRACTIONAL_WEIGHT** — ``dist`` weights must be integer
    expressions: no real literals and no division.

    **Rationale**: Integer division truncates toward zero, so a weight of
    ``1/2`` evaluates to 0 and the value is never picked. Real weights such as
    ``0.5`` are tool-dependent: some simulators round them, others error out.
    A fractional weight on a range with ``:=`` is usually an attempt to spread
    one unit of weight across the range, which is what ``:/`` does.

    **Violation**::

        constraint c { data dist {111 := 1/2, 222 := 1/2, 333 := 1}; }  // 333 always
        constraint c { data dist {111 := 0.5, 222 := 0.5, 333 := 1}; }  // tool-dependent
        constraint c { data dist {[0:10] := 1/11, 12 := 1}; }           // 12 always

    **Correct usage**::

        constraint c { data dist {111 := 25, 222 := 25, 333 := 50}; }
        constraint c { data dist {[0:10] :/ 1, 12 := 1}; }

    **Severity**: ERROR for real weights and literal divisions that truncate
    to 0; WARNING for other truncating or non-constant divisions.
    """

    def __init__(self, linter):
        self.linter = linter
        self.ruleID = "CNST_DIST_FRACTIONAL_WEIGHT"

    def parseIntLiteral(self, node):
        """Returns the value of a plain decimal literal node, else None."""
        litText = node.text.strip().replace("_", "")
        if litText.isdigit():
            return int(litText)
        return None

    def checkWeight(self, weightNode):
        """
        Classifies a dist weight expression.

        Returns (severity, reason), or None if the weight is fine.
        """
        if not hasattr(weightNode, "iter_find_all"):
            return None

        if list(weightNode.iter_find_all({"tag": "TK_RealTime"})):
            return ("ERROR", "is a real literal; dist weights must be integral")

        divNodes = [
            binNode
            for binNode in weightNode.iter_find_all({"tag": "kBinaryExpression"})
            if len(binNode.children) == 3
            and getattr(binNode.children[1], "tag", "") == "/"
        ]

        for divNode in divNodes:
            lhsVal = self.parseIntLiteral(divNode.children[0])
            rhsVal = self.parseIntLiteral(divNode.children[2])

            if lhsVal is None or rhsVal is None:
                return (
                    "WARNING",
                    "uses division with a non-constant operand, which "
                    "truncates and may evaluate to 0 at runtime",
                )

            if rhsVal == 0:
                continue

            if lhsVal // rhsVal == 0:
                return (
                    "ERROR",
                    f"truncates to 0 ({divNode.text.strip()} == 0 in integer "
                    "arithmetic), so the value is never picked",
                )

            if lhsVal % rhsVal != 0:
                return (
                    "WARNING",
                    f"is silently truncated ({divNode.text.strip()} == "
                    f"{lhsVal // rhsVal} in integer arithmetic)",
                )

        return None

    def apply(
        self,
        filePath: str,
        data: AsFigoLintRule.VeribleSyntax.SyntaxData,
    ):
        if data.tree is None:
            return

        for distNode in data.tree.iter_find_all({"tag": "kDistribution"}):
            for itemNode in distNode.iter_find_all({"tag": "kDistributionItem"}):
                itemChildren = list(itemNode.children)

                # Find the ':=' or ':/' leaf; the weight follows it
                opIdx = None
                for idx, child in enumerate(itemChildren):
                    if getattr(child, "tag", "") in (":=", ":/"):
                        opIdx = idx
                        break

                if opIdx is None or opIdx + 1 >= len(itemChildren):
                    continue

                distOp = itemChildren[opIdx].tag
                weightNode = itemChildren[opIdx + 1]

                result = self.checkWeight(weightNode)
                if result is None:
                    continue

                severity, reason = result
                isRange = getattr(itemChildren[0], "tag", "") == "kValueRange"

                if isRange and distOp == ":=":
                    fixSuggestion = (
                        "Use ':/' to spread an integer weight across the "
                        "whole range, e.g. '[lo:hi] :/ 1'."
                    )
                else:
                    fixSuggestion = (
                        "Use integer weights scaled to the desired ratio, "
                        "e.g. '111 := 25, 222 := 75' instead of fractions."
                    )

                message = self.formatViolationMessage(
                    description=(
                        f"dist weight '{weightNode.text.strip()}' {reason}."
                    ),
                    code_snippet=distNode.text,
                    fix_suggestion=fixSuggestion,
                )
                self.linter.logViolation(self.ruleID, message, severity=severity)
