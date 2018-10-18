class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


class Solution0:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        res = []
        carry = 0

        while l1 is not None and l2 is not None:
            s = l1.val + l2.val + carry
            l1, l2 = l1.next, l2.next

            carry = s // 10
            res.append(s % 10)

        while l1 is not None:
            s = l1.val + carry
            l1 = l1.next

            carry = s // 10
            res.append(s % 10)

        while l2 is not None:
            s = l2.val + carry
            l2 = l2.next

            carry = s // 10
            res.append(s % 10)

        if carry == 1:
            res.append(1)

        return res


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        l01 = ""
        while l1 is not None:
            l01 += str(l1.val)
            l1 = l1.next

        l02 = ""
        while l2 is not None:
            l02 += str(l2.val)
            l2 = l2.next

        return [int(s) for s in str(int(l01) + int(l02))]
