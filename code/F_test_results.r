library('grid')
library("ggplot2")
library("RColorBrewer")

data <- read.csv('R_test_results.txt', sep="\t", header=FALSE)

colnames(data) <- c("Filename", "Method", "Score1", "Score2", "FScore")
data$Analysis <- gsub('^D_test_(.*?)-.*$', '\\1', data$Filename)

method_colors <- rev(brewer.pal(n=length(unique(data$Method)), "Spectral"))

analysis_colors <- rev(brewer.pal(n=length(unique(data$Analysis)), "Set1"))


# specify factor ordering for methods
data$Method <- factor(data$Method, levels=c(
    "Turchin", "SCA", "Edit Distance", "LexStat", "Infomap"  
))

# re-creating original figure "I_detailed_results.pdf"
p <- ggplot(data, aes(y=FScore, x=Method, fill=Method))
p <- p + geom_bar(stat="identity", position=position_dodge())
p <- p + ylim(0.0, 1.0)
p <- p + ylab("F-Score")
p <- p + facet_wrap(~Analysis, ncol=6)
p <- p + scale_fill_manual(values=method_colors)
p <- p + theme_minimal()
p <- p + theme(panel.margin.x=unit(1.5, "lines"))
p <- p + theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    panel.grid.minor=element_blank(),
    panel.grid.major=element_blank()
)

pdf('R_test_results.pdf')
print(p)
dev.off()


# Boxplot by Method
p <- ggplot(data, aes(y=FScore, x=Method, fill=Method))
p <- p + geom_boxplot() + coord_flip()
p <- p + ylab("F-Score")
p <- p + scale_fill_manual(values=method_colors)
p <- p + theme_minimal()

pdf('R_test_results-boxplot-by-method.pdf')
print(p)
dev.off()


# Boxplot by Dataset
p <- ggplot(data, aes(y=FScore, x=Analysis, fill=Analysis))
p <- p + geom_boxplot(aes(alpha=0.1)) + coord_flip()
p <- p + scale_fill_manual(values=analysis_colors)
p <- p + theme_minimal()

pdf('R_test_results-boxplot-by-dataset.pdf')
print(p)
dev.off()


# F-Score facet by analysis

p <- ggplot(data, aes(x=FScore, y=Method, color=Method, group=Analysis))
p <- p + geom_point(aes(shape = Method), size=5)
p <- p + facet_grid(Analysis~.)
p <- p + scale_fill_manual(values=method_colors)
p <- p + theme_minimal()


pdf('R_test_results-scatter-by-dataset.pdf')
print(p)
dev.off()

