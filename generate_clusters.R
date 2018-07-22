library(tidyr)
library(Rtsne)
##read data
##run in shell to proccess data (remove headeres, add unique names to the first row of each line )
### for file in ./*.csv 
#### do 
#### name=$( basename $file ".csv" ); 
#### cat $file | grep -v "Trait Name," | sed -E "s/(.+)/$name,\1/gi" >> proccessed.csv
###done
x = read.csv("./processed/proccessed.csv", sep = ",", header = F)
##show first 10 lines of the dataframe 
head(x)
##removes any rows with NA
x = x[complete.cases(x),]
##adds column names
names(x)= c("id", 'feat', 'score', 'type1' , 'type2', 'snp')
##removes the NA column 
x$`NA` = NULL
##makes a dummy variable out of the type1/ type2 columns 
x$type1 = as.numeric(as.factor(x$type1))
x$type = as.numeric(as.factor(x$type2))
##converts features into a factor from a string 
x$feat = as.factor(x$feat)
##creates a new dataframe (x2) that has all rows and the 1st ,2nd and 4th columns of the x df
x2 = x[,c(1,2,4)]
##converts the dataframe from long to wide 
x.wide = as.data.frame(spread(data = x2, 
                              key = feat, 
                              value = type1, 
                              fill = 'Severe'  ))
##writes the dataframe out to a file 
write.table(x.wide, "data.matrix.tab" , sep = " ", col.names = T, row.names = T, quote = F )
##sets the row names to the id column of the x.wide dataframe 
rownames(x.wide) = x.wide$id
##removes the id column of the dataframe (since these are names, they should not be used in the numeric analysis)
x.wide$id = NULL
##runs tsne 
z.tsne = Rtsne(data.matrix(x.wide), dims = 3, check_duplicates = F , perplexity = .1, max_iter = 1000, theta = 0, pca = F) 
##grabs the reduced dimensions from the z.tsne object 
y = as.data.frame(z.tsne$Y)
library(plotly)
##run kkn clustering on the tsne reduced dimension dataset 
y.kmeans =  kmeans(y, centers = 2 )
##adds a column to y with the cluster classifications 
y$cluster = y.kmeans$cluster
##3d scatterplot
plot_ly(y, x = y[,1], y = y[,2], z = y[,3], color = y$cluster )
library(gplots)
##heatmap 
x.wide.t = t(x.wide) #t() transposes the matrix (flipping the matrix)
heatmap.2(data.matrix(x.wide.t), trace= "none")
library(qgraph)
##generates a distance matrix between each row of the dataframe 
dist_m = as.matrix(dist(t(x.wide.t)))
dist_mi <- 1/dist_m
mat = dist_mi
##converts the distance matrix from wide to long 
library(reshape2)
df = as.data.frame(subset(melt(mat), value!=0))
##removes 'inf' values from the df 
df = df[!is.infinite(df$value),]
#histogram of the distances 
hist(df$value)
##remove any rows with values less than or equal to .1 
df = df[df$value > .1, ]
library(networkD3)
##makes network dataframe
d2 = data.frame(df$Var1, df$Var2)
names(d2) = c("src", "target")
#makes simple interactive network 
simpleNetwork( d2)
#makes ugly network
qgraph(dist_mi, layout='spring', vsize=3)

