#Plotting the feature
ylims <- range(cough$V2, blender$V2, vaccum$V2, doorBell$V2)
plot(cough$V2, col="red", main = "Energy", ylim = ylims)
points(blender$V2, col="green")
points(vaccum$V2, col="blue")
points(doorBell$V2, col="orange")

#Plotting the means of the data
plot(mean(cough$V2), pch=19, col="red", 
     #ylim = c(0, 0.3), 
     main = "Mean of ZC", ylab = "Mean")
points(mean(blender$V2), pch=19, col="green")
points(mean(vaccum$V2), pch=19, col="blue")
points(mean(doorBell$V2), pch=19, col="orange")
