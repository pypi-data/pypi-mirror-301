import numpy as np
import robotic as ry

print(ry.compiled())

C = ry.Config()
C.addFile(ry.raiPath('../rai-robotModels/scenarios/pandaSingle.g'))

midpoint = np.array([-0.105, 0.4, 0.705-.025+.3])
C.addFrame("box") \
    .setPosition(midpoint) \
    .setShape(ry.ST.ssBox, size=[0.04, 0.12, 0.04, 0.001]) \
    .setColor([0, 0, 1]) \
    .setContact(1) \
    .setMass(.1)

print('position:', C.frame('box').getPosition())
C.view(True)

bot = ry.BotOp(C, False)
# bot.home(C)

qHome = bot.get_qHome()
q0 = qHome.copy()
q1 = q0.copy()
q1[1] = q1[1] + .2
# print(q0, q1)

bot.moveTo(q1)

while bot.getTimeToEnd()>0:
    bot.sync(C, .1)

print('position:', C.frame('box').getPosition())
C.view(True)
