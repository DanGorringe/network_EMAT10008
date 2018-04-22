primGif:
	convert -delay 35 -loop 0 ./primsGif/*.png animated.gif

ghostGif:
	convert -delay 35 -loop 0 ./ghostGif/*.png animated.gif

# Python to save images nicely
# SaveNetworkImage(ghostingDic,"./ghostGif/"+format(i,'03d')+".png")
