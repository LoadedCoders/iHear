#Plotting the feature
ylims <- range(flushing$V34, boilingWater$V34)
plot(flushing$V34, col="red", main = "MFCC", ylim = ylims)
lines(flushing$V34, col="red")
points(boilingWater$V34, col="green")
lines(boilingWater$V34, col="green")

#Plotting the means of the data
lims <- range(mean(flushing$V34), sd(flushing$V34), mean(boilingWater$V34),sd(boilingWater$V34))
plot(mean(flushing$V34), pch=19, col="red", 
     #ylim = c(0, 0.3), 
     main = "Mean of ZC", ylab = "Mean", ylim = lims)
points(sd(flushing$V34), pch=22, col="red")
points(mean(boilingWater$V34), pch=19, col="green")
points(sd(boilingWater$V34), pch=22, col="green")


