21/12
Melhora da interface e do código dela, principalmente a barra de progresso, a qual quebramos em duas etapas
Otimização do scanner, trocando o rglob para os.scandir

24/12
Remoção do módulo de IA pois é irrisório, apenas consome desempenho dos processos
Remoção da camada de segurança do scanner para incrementar no desempenho (Eram funções redundantes)
Remoção do boiler plaite da sidebar
adição da aba de configurações para adição de caminhos para a blacklist
Integração funcional com o método de adição da classe blacklist

25/12
Integração final da blacklist com o scanner
Unificação da barra de progresso, fica dividida em etapas, e permite modificação dos pesos das etapas
Adição de mais uma etapa, sendo a de mover, a última etapa
Remoção da aba de relatórios como tentativa de aumentar o desempenho de inicialização da interface gráfica
remoção da estrutura models para o banco de dados e remoção do próprio, já que a aplicação está pesada demais para aguentar mais uma funcionalidade
