classesFull <- unique(featuresv1$V1)
classes <- sample(classesFull, 10)
plotFeature <- function (feat) {
  lim <- range(featuresv1[,feat])
  
  plot(1, ylim = lim, xlim = c(1,40), xlab = "Sample No", ylab = "")
  for (i in classes) {
    indices <- which(featuresv1$V1==i)
    points(featuresv1[indices, feat], col=i, pch=5)
  }
}

plotFeature(2)