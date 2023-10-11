# Automação Web - Aplicação Mercado de Trabalho
### Projeto de automação web - aplicação no mercado de trabalho

Imagine que você trabalha na área de compras de uma empresa e precisa fazer uma comparação de fornecedores para os seus insumos/produtos.
Nessa hora, você vai constantemente buscar nos sites desses fornecedores os produtos disponíveis e o preço, afinal, cada um deles pode fazer promoção em momentos diferentes e com valores diferentes.
O objetivo é que o script em python perceba e procure produtos abaixo de um preço limite definido por você, trazendo os produtos mais baratos e atualizar isso em planilha.
Em seguida, envia um e-mail com a lista dos produtos abaixo do seu preço máximo de compra.
No nosso projeto, vamos fazer om produtos comuns em sites como Google Shopping e Buscapé, mas a ideia é a mesma para outros sites.

### O que temos disponível?

Planilha de produtos, com nome dos produtos, o preço máximo e o preço mínino (para evitar produtos "errados" ou "baratos demais para ser verdade", e termos que vamos querer evitar nas nossas buscas.

### O que devemos fazer?

Criar uma planilha com a coluna do menor preço encontrado e link onde foi encontrado esse preço. Depois disso, enviar um e-mail com a notificação de menor preço encontrado e o link da compra.
Caso o preço esteja 20% ou mais de desconto em relação ao preço original. (Vou usar o e-mail joaofcfreire@gmail.com para a finalidade do projeto).

