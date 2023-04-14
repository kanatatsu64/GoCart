from cart import Goal, Block, Field, Cord

block1 = Block([])
field1 = Field(Goal(Cord(6, 6)), block1, width=7, height=7)

block2 = Block([Cord(2, 0), Cord(2, 1), Cord(2, 2), Cord(2, 3)])
field2 = Field(Goal(Cord(6, 6)), block2, width=7, height=7)

block3 = Block([Cord(2, 0), Cord(2, 1), Cord(2, 2), Cord(2, 3), Cord(4, 6), Cord(4, 5), Cord(4, 4)])
field3 = Field(Goal(Cord(6, 6)), block3, width=7, height=7)

# anti-leftmost
block4 = Block([])
field4 = Field(Goal(Cord(5, 5)), block4, width=7, height=7)

# anti-mapping
block5 = Block([Cord(3, 2), Cord(3, 3), Cord(4, 3), Cord(4, 2), Cord(1, 5), Cord(2, 5), Cord(3, 5), Cord(4, 5), Cord(5, 5), Cord(6, 5)])
field5 = Field(Goal(Cord(6, 6)), block5, width=7, height=7)

block6 = Block([Cord(3, 0), Cord(3, 1), Cord(3, 2), Cord(3, 3), Cord(4, 3), Cord(5, 3), Cord(6, 3)])
field6 = Field(Goal(Cord(6, 6)), block6, width=7, height=7)
