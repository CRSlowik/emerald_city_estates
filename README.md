# emerald_city_estates

## Problema de negócio
  A Emerald City Estates é uma empresa fictícia que atua na compra e venda de imóveis, pautando sua estratégia na realização de estudos para identificação de oportunidades de investimento. Com o objetivo de maximizar os lucros, busca por imóveis com potencial de valorização para adquirir e posteriormente vender.
  
  No momento, o desafio da empresa consiste em identificar as melhores oportunidades na cidade de Seattle. Para tanto, dispõe de uma base de dados contendo informações de 21.613 imóveis colocados à venda entre 02/05/2014 e 27/05/2015. A partir desses dados, a empresa busca responder à seguinte pergunta: quais são os imóveis com maior potencial de retorno financeiro?

## Premissas assumidas
### Tratamento de Dados Faltantes e Duplicados:
  Para coletar e tratar os dados, fora considerado as características do negócio e a questão em pauta. Verificou-se que nenhum dos atributos do dataset possui dados faltantes, entretanto, encontramos 177 imóveis duplicados indicando vendas múltiplas em períodos distintos. Ao analisar a variação dos atributos, concluiu-se que apenas o preço varia entre as vendas dos mesmos imóveis. Por isso, fora optador manter os imóveis duplicados no conjunto de dados para fins de análise de vendas por período.

### Tratamento de Valor Outlier para número de quartos:
  Fora identificado um valor de 33 quartos em um imóvel do dataset e verificamos a veracidade do dado. Ao avaliar outros imóveis com faixa de preço, tamanho interno, quantidade de banheiros e andares semelhantes, concluiu-se que o valor de 33 é um possível erro de digitação e será substituído por 3.

### Tratamento de Imóveis com zero quartos ou banheiros:
  Há 16 imóveis na base de dados sem quartos ou banheiros. Supõe-se que estão corretos e não serão excluídos, pois podem não ter tido ainda um uso residencial. É importante ressaltar que a ausência de quartos ou banheiros pode resultar em preços abaixo da média em sua localização, o que pode representar uma oportunidade para a empresa.

Para garantir a qualidade dos dados e análises, fora feita uma análise rigorosa no tratamento de dados faltantes, duplicados e outliers. Espera-se, portanto, que os resultados obtidos sejam mais precisos e confiáveis.
  
## Planejamento da solução
  Inicialmente, foram consideradas as características do negócio e a questão proposta, para então realizar a coleta dos dados e iniciar o tratamento dos mesmos. A limpeza dos dados foi realizada com o objetivo de eliminar outliers ou qualquer outro tipo de informação que pudesse interferir na análise. Após a conclusão desses procedimentos, foi iniciada uma análise exploratória dos dados para elaborar insights que identificassem quais as características mais relevantes para o crescimento financeiro dos imóveis, permitindo a seleção das melhores oportunidades de retorno financeiro.
  
  Por fim, foi elaborado um dashboard na nuvem para a apresentação dos insights e a visualização dos imóveis recomendados por meio de um mapa. O dashboard possibilita a visualização clara e objetiva das informações coletadas, facilitando a tomada de decisões estratégicas pela empresa. 
  
## Principais Insights
   1. Imóveis reformados são 43,9% mais caros que imóveis velhos.
   2. Imóveis com 3 banheiros ou mais se mostraram 105,6% mais caros do que imóveis com menos de 3 banheiros
   3. Imóveis com 3 quartos ou mais se mostraram 42,26% mais caros do que imóveis com menos de 3 quartos
   4. Imóveis com vista para à água são 212,6% mais caros que imóveis sem vista para à água
   5. Imóveis vendidos na primavera são 6,5% mais caros que imóveis vendidos no inverno
   
## Resultados
   Com base nas análises realizadas, verificou-se que o crescimento anual dos imóveis se manteve baixo, em torno de 0,5% de aumento. Diante disso, a busca por imóveis com preços abaixo da mediana se apresenta como a melhor alternativa para aquisição.
 
 Além disso, os imóveis com vista para água se mostraram interessantes, já que apresentam um preço médio 212,6% mais alto do que os demais. Apesar de demandarem um maior investimento para aquisição, a compra de um imóvel com preço abaixo da mediana e sua revenda por um valor próximo à mediana pode gerar grandes lucros. Com base nesse critério, foram selecionados 73 imóveis que podem ser comercializados dessa forma, gerando um lucro em torno de 42,4 milhões de dólares.
 
 Considerando ainda que imóveis reformados são, em média, 43,9% mais caros que os imóveis com mais de 10 anos que não foram reformados, foram selecionados 1660 imóveis abaixo da mediana de preços que podem ser reformados. Foi levada em conta também a possibilidade de adicionar mais quartos e banheiros, visto que imóveis com 3 ou mais quartos são 42,46% mais caros e imóveis com 3 ou mais banheiros são 105,6% mais caros. Os imóveis selecionados apresentam menos de 3 quartos e 3 banheiros. A venda desses imóveis pela mediana, sem levar em conta a reforma, pode gerar um lucro em torno de 251,2 milhões de dólares.
 
 Por fim, considerando que a compra dos imóveis seja realizada no inverno e a venda na primavera, é possível obter um aumento de 6,5%. 
 
 Também, fora disponíbilizado um Dashboard na nuvem com informações detalhadas sobre a análise realizada, incluindo os principais critérios que afetam os preços dos imóveis, e um mapa com os melhores imóveis da cidade. Disponível em: [https://projects-emerald-city-estates.streamlit.app/](https://projects-emerald-city-estates.streamlit.app/)

## Conclusão
  Os objetivos propostos foram alcançados de maneira satisfatória, pois foi possível elaborar uma lista de recomendações de imóveis para compra que atende aos requisitos definidos pela Emerald City Estates. Adicionalmente, foram identificados 5 insights valiosos a partir da análise da base de dados estudada, o que pode contribuir para a tomada de decisões futuras da empresa. Por fim, todas as análises realizadas foram disponibilizadas em uma aplicação na nuvem, o que permite fácil acesso e consulta das informações obtidas.
  
## Próximos passos
  Para potenciais atualizações futuras, seria vantajoso considerar a implementação de um algoritmo de aprendizado de máquina para otimizar o lucro e automatizar a análise de novos imóveis.
  
  
  
  
  
