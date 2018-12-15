# Rect-Collision 

It is a sample python file that describes about the side-based rect collision response. Its simple and easy to understand.

# Concept

Basically how it works is when you move a rect, you first move along the X axis, test for a collision, move out, then move along the Y axis, test for a collision, and move out. This prevents the infamous "corner-catching" bug, and lets you move smoothly along walls.
 
# Final Output

![side based rect collision](/rectcollision/rect.png)

The final output will be displayed as the above figure.
If you got the same output as above. Then you are all set.

# Working

As this file is to describe the side-based rect collision. This is actually implemented as a game for better understanding. The block interacts with your keyboard and moves with the help of arrows.
When you finally reach the other end and interact with the other block.
Then **you win!** will be displayed in the terminal.
