library('grid')
library("ggplot2")
library("RColorBrewer")

data <- read.csv('R_training_results.txt', sep="\t", header=FALSE)

colnames(data) <- c("Filename", "Analysis", "Method", "Threshold", "Precision", "Recall", "HMean")
# filter
data <-  data[data$Method %in% c("mcl", "turchin") == FALSE, ]

# rename
data$Method <- as.character(data$Method)
data[data$Method == 'sca', ]$Method <- 'SCA'

method_colors <- rev(brewer.pal(n=length(unique(data$Method)), "Spectral"))
analysis_colors <- rev(brewer.pal(n=length(unique(data$Analysis)), "Set1"))

# specify factor ordering for methods
data$Method <- factor(data$Method, levels=c(
    "SCA", "edit", "lexstat", "infomap"  
))



p <- ggplot(data, aes(x=Threshold, y=HMean, fill=Method, group=Threshold))
p <- p + geom_crossbar(aes(alpha=0.1))
p <- p + facet_wrap(~Method)
p <- p + ylim(0.0, 1.0)
p <- p + xlim(0.0, 1.0)
p <- p + scale_fill_manual(values=analysis_colors)
p <- p + theme_minimal()
p <- p + theme(legend.position="none")

pdf('R_training_results.pdf')
print(p)
dev.off()

