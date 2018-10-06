from itertools import product

class Solution:
    def letterCasePermutation(self, S):
        """
        :type S: str
        :rtype: List[str]
        """
        # S=input()
        l = [(c, c.upper()) if not c.isdigit() else (c,) for c in S.lower()]

        return ["".join(item) for item in product(*l)]

