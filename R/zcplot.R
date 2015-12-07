#Plotting the feature
plot(cough$V1, col="red", main = "Features")
points(blender$V1, col="green")
points(vaccum$V1, col="blue")
points(doorBell$V1, col="orange")

#Plotting the means of the data
plot(mean(cough$V1), pch=19, col="red", ylim = c(0, 0.3), main = "Mean of ZC", ylab = "Mean")
points(mean(blender$V1), pch=19, col="green")
points(mean(vaccum$V1), pch=19, col="blue")
points(mean(doorBell$V1), pch=19, col="orange")
