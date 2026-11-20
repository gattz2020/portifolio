#Chamar bibliotecas

install.packages('ggplot2')
install.packages('ddplyr')

# Fim das chamadas das bibliotecas

library(ggplot2)
library(ddplyr)

#Carregar os dados

saude_df <- read.csv("saúde_data.csv")
logistic_df <- read.csv("logistica_Data.csv")
terceiro_setor_df <- read.csv("terceiro_setor_data.csv")

saude <-