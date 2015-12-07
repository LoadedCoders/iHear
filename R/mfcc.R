# old.par <- par(mfrow=c(1,5))

lims <- range(cough$V9, cough$V11, cough$V13,
              cough$V15, cough$V17, cough$V19,
              cough$V21)

plot(cough$V9, col="blue", ylim = lims)
points(cough$V11, col="red")
points(cough$V13, col="yellow")
points(cough$V15, col="brown")
points(cough$V17, col="grey")
points(cough$V19, col="grey")
points(cough$V21, col="orange")
# par(old.par)