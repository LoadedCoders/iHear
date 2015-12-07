#Plotting the feature
ylims <- range(cough$V4, blender$V4, vaccum$V4, doorBell$V4)
plot(cough$V4, col="red", main = "MFCC", ylim = ylims)
lines(cough$V4, col="red")
points(blender$V4, col="green")
lines(blender$V4, col="green")
points(vaccum$V4, col="blue")
lines(vaccum$V4, col="blue")
points(doorBell$V4, col="orange")
lines(doorBell$V4, col="orange")

#Plotting the means of the data
plot(mean(cough$V4), pch=19, col="red", 
     #ylim = c(0, 0.3), 
     main = "Mean of ZC", ylab = "Mean")
points(mean(blender$V4), pch=19, col="green")
points(mean(vaccum$V4), pch=19, col="blue")
points(mean(doorBell$V4), pch=19, col="orange")
