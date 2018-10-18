class Solution0:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        length = len(nums)
        for i in range(length):
            for j in range(i + 1, length):
                if nums[i] + nums[j] == target:
                    return [i, j]


class Solution1:
    def twoSum(self, nums, target):
        a = {nums[i]: i for i in range(len(nums))}

        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in a.keys() and a[complement] != i:
                return [i, a[complement]]


class Solution:
    def twoSum(self, nums, target):
        a = dict()
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in a.keys() and a[complement] != i:
                return [i, a[complement]]
            a[nums[i]] = i


print(Solution().twoSum([3, 3], 6))
