# 🎟️ Sistema de Cupons de Desconto - Guia de Teste

## ✅ Sistema Implementado com Sucesso!

O sistema de cupons de desconto foi completamente implementado no "Cantos de Papel". Agora você pode oferecer descontos aos seus clientes durante o checkout.

---

## 📋 Funcionalidades Implementadas

### Backend (Completo ✅)
- ✅ **Modelo Cupom**: Com validação de datas, limites de uso, valor mínimo
- ✅ **Modelo UsoCupom**: Rastreamento de cada uso por utilizador
- ✅ **Validação AJAX**: Endpoint `/validar-cupom/` para validação em tempo real
- ✅ **Integração no Checkout**: Aplicação automática do desconto ao criar pedido
- ✅ **Admin Interface**: Interface visual com status coloridos e estatísticas

### Frontend (Completo ✅)
- ✅ **Input de Cupom**: Campo estilizado no checkout
- ✅ **Validação em Tempo Real**: AJAX sem recarregar página
- ✅ **Feedback Visual**: Mensagens de erro/sucesso
- ✅ **Cálculo Dinâmico**: Atualização automática do total
- ✅ **Design Outonal**: Integrado com o tema do site (#c87941, #faf8f5)

---

## 🎫 Cupons de Teste Disponíveis

Foram criados 6 cupons para teste. Use qualquer um destes códigos:

### 1. **VIP25** - Desconto VIP Exclusivo
- 💰 **Desconto**: 25%
- 📦 **Pedido mínimo**: €40.00
- 🔢 **Limite**: 50 utilizações
- ⏰ **Válido**: 14 dias (até 20 Nov 2025)
- 👤 **Por utilizador**: 1 uso

### 2. **BLACKFRIDAY2025** - Black Friday Especial
- 💰 **Desconto**: 20%
- 📦 **Pedido mínimo**: Nenhum
- 🔢 **Limite**: 500 utilizações
- ⏰ **Válido**: 7 dias (até 13 Nov 2025)
- 👤 **Por utilizador**: 2 usos

### 3. **NATAL2025** - Promoção de Natal
- 💰 **Desconto**: 15%
- 📦 **Pedido mínimo**: €30.00
- 🔢 **Limite**: 200 utilizações
- ⏰ **Válido**: 45 dias (até 21 Dez 2025)
- 👤 **Por utilizador**: 3 usos

### 4. **OUTONO2025** - Especial Outono
- 💰 **Desconto**: 10%
- 📦 **Pedido mínimo**: €20.00
- 🔢 **Limite**: 100 utilizações
- ⏰ **Válido**: 30 dias (até 6 Dez 2025)
- 👤 **Por utilizador**: 2 usos

### 5. **GRANDE10** - Desconto Grande
- 💰 **Desconto**: €10.00 (valor fixo)
- 📦 **Pedido mínimo**: €50.00
- 🔢 **Limite**: 300 utilizações
- ⏰ **Válido**: 90 dias (até 4 Fev 2026)
- 👤 **Por utilizador**: 5 usos

### 6. **BEMVINDO5** - Bem-vindo
- 💰 **Desconto**: €5.00 (valor fixo)
- 📦 **Pedido mínimo**: €15.00
- 🔢 **Limite**: 1000 utilizações
- ⏰ **Válido**: 60 dias (até 5 Jan 2026)
- 👤 **Por utilizador**: 1 uso

---

## 🧪 Como Testar

### Passo 1: Adicionar Livros ao Carrinho
1. Aceda a http://127.0.0.1:8000/livros/
2. Adicione alguns livros ao carrinho
3. Vá para o carrinho e clique em "Finalizar Compra"

### Passo 2: Aplicar Cupom no Checkout
1. No checkout, localize a seção **"🎟️ Cupom de Desconto"**
2. Digite um dos códigos acima (ex: **OUTONO2025**)
3. Clique em **"Aplicar"**
4. Observe:
   - ✅ Mensagem de sucesso em verde
   - 💰 Desconto aplicado no resumo
   - 📊 Total atualizado automaticamente

### Passo 3: Testar Validações

**Teste 1: Código Inválido**
- Digite: `INVALIDO123`
- Resultado esperado: ❌ "Cupom inválido ou não encontrado"

**Teste 2: Valor Mínimo**
- Use cupom VIP25 com carrinho < €40
- Resultado esperado: ❌ "Valor mínimo do pedido: €40.00"

**Teste 3: Cupom Expirado**
- (Aguarde expiração ou teste no admin)

**Teste 4: Limite de Usos**
- Use o mesmo cupom VIP25 2 vezes com o mesmo utilizador
- Resultado esperado: ❌ "Já utilizou este cupom o máximo de vezes permitido"

**Teste 5: Remover Cupom**
- Aplique um cupom
- Clique no **✕** ao lado do código
- Resultado esperado: Total volta ao valor original

---

## 👨‍💼 Admin Interface

Aceda ao painel administrativo para gerir cupons:

### Ver Cupons
1. Login: http://127.0.0.1:8000/admin/
2. Navegue até **Members > Cupons**
3. Veja lista com:
   - Código do cupom
   - Valor/Percentagem
   - Status (✓ Válido / ✗ Inválido)
   - Período de validade
   - Usos (com código de cores)

### Criar Novo Cupom
1. Clique em **"Adicionar Cupom"**
2. Preencha os campos:
   - **Código**: Use maiúsculas (ex: VERAO2026)
   - **Descrição**: Explicação do cupom
   - **Tipo de desconto**: Percentagem ou Valor fixo
   - **Valor**: 10 (para 10%) ou 5.00 (para €5)
   - **Datas**: Início e fim da validade
   - **Uso máximo**: Total de utilizações permitidas
   - **Uso por utilizador**: Máximo por pessoa
   - **Valor mínimo pedido**: Requisito mínimo de compra
3. Clique em **"Guardar"**

### Estatísticas de Uso
- No detalhe de cada cupom, veja o **histórico de usos**
- Informações incluem:
  - Utilizador que usou
  - Pedido associado
  - Valor do desconto aplicado
  - Data de uso

---

## 🎨 Design e UX

### Cores Outonais Integradas
- **Fundo**: #faf8f5 (bege quente)
- **Bordas**: #e8d5c4 (bege outonal)
- **Botão**: #c87941 (terra cotta)
- **Sucesso**: Verde suave
- **Erro**: Vermelho suave

### Animações Suaves
- Transições de 0.3s nos botões
- Hover effects elegantes
- Feedback visual imediato

### Responsividade
- Desktop: Layout de 2 colunas
- Mobile: Layout vertical otimizado
- Touch-friendly para tablets

---

## 🔧 Detalhes Técnicos

### Estrutura de Arquivos Modificados

```
projeto_livraria/
├── members/
│   ├── models.py          ✅ Adicionado: Cupom, UsoCupom
│   ├── admin.py           ✅ Adicionado: CupomAdmin, UsoCupomAdmin
│   ├── views.py           ✅ Adicionado: validar_cupom(), checkout atualizado
│   ├── urls.py            ✅ Adicionado: path('validar-cupom/')
│   ├── templates/
│   │   └── checkout.html  ✅ Seção de cupom + JavaScript AJAX
│   └── management/
│       └── commands/
│           └── create_cupons.py  ✅ Script de criação de cupons
└── migrations/
    ├── 0008_cupom_usocupom.py           ✅ Aplicada
    └── 0009_pedido_cupom_desconto.py    ✅ Aplicada
```

### Modelos de Base de Dados

**Cupom**:
```python
- codigo (CharField, unique)
- descricao (TextField)
- tipo_desconto (CharField: 'percentagem' ou 'valor_fixo')
- valor (DecimalField)
- data_inicio, data_fim (DateTimeField)
- ativo (BooleanField)
- uso_maximo (IntegerField)
- uso_por_utilizador (IntegerField)
- valor_minimo_pedido (DecimalField)
- vezes_usado (IntegerField)
- data_criacao (DateTimeField auto)
```

**UsoCupom**:
```python
- cupom (ForeignKey)
- utilizador (ForeignKey)
- pedido (ForeignKey)
- data_uso (DateTimeField auto)
- valor_desconto (DecimalField)
```

**Pedido** (atualizado):
```python
+ cupom (ForeignKey, null=True)
+ desconto_cupom (DecimalField, default=0)
```

### Métodos de Validação

```python
# Cupom.esta_valido()
- Verifica se está ativo
- Valida data de início e fim
- Confirma se não atingiu uso máximo

# Cupom.pode_usar_utilizador(user)
- Conta quantas vezes o utilizador já usou
- Compara com uso_por_utilizador
- Retorna (bool, mensagem)

# Cupom.calcular_desconto(valor_pedido)
- Aplica percentagem ou valor fixo
- Garante que desconto ≤ valor_pedido
```

---

## 📊 Exemplos de Uso Real

### Cenário 1: Cliente Novo (BEMVINDO5)
```
Carrinho: €18.00
Cupom: BEMVINDO5 (-€5.00)
Subtotal: €18.00
IVA (23%): €4.14
Desconto: -€5.00
TOTAL: €17.14 (economizou €5.00!)
```

### Cenário 2: Compra Grande (VIP25)
```
Carrinho: €80.00
Cupom: VIP25 (-25% = €20.00)
Subtotal: €80.00
IVA (23%): €18.40
Desconto: -€20.00
TOTAL: €78.40 (economizou €20.00!)
```

### Cenário 3: Black Friday (BLACKFRIDAY2025)
```
Carrinho: €45.00
Cupom: BLACKFRIDAY2025 (-20% = €9.00)
Subtotal: €45.00
IVA (23%): €10.35
Desconto: -€9.00
TOTAL: €46.35 (economizou €9.00!)
```

---

## 🚀 Próximos Passos Sugeridos

1. **Email Marketing**:
   - Enviar cupons por email para clientes registados
   - Newsletter com código exclusivo

2. **Cupons Personalizados**:
   - Cupons únicos por utilizador (ex: JOAO2025)
   - Cupons de aniversário automáticos

3. **Gamificação**:
   - Cupons por compra acumulada
   - Programa de fidelidade com pontos

4. **Analytics**:
   - Dashboard com estatísticas de cupons
   - Cupons mais populares
   - ROI de promoções

5. **Integração Social**:
   - Compartilhar cupom nas redes sociais
   - Cupons por referência de amigos

---

## 🎉 Sistema 100% Funcional!

O sistema de cupons está completamente operacional e pronto para uso em produção. Todos os cupons de teste estão ativos e podem ser utilizados imediatamente.

**Desenvolvido com**: Django 5.2.6, JavaScript vanilla, CSS3, cores outonais (#c87941, #faf8f5)
**Data**: Novembro 2025
**Projeto**: Cantos de Papel - Livraria Online

---

## ❓ Resolução de Problemas

**Problema**: Cupom não aplica
- ✅ Verifique se está autenticado
- ✅ Confirme valor mínimo do pedido
- ✅ Veja no admin se cupom está ativo

**Problema**: Mensagem de erro genérica
- ✅ Verifique console do navegador (F12)
- ✅ Confirme que servidor está rodando
- ✅ Teste endpoint diretamente: POST /validar-cupom/

**Problema**: Total não atualiza
- ✅ Limpe cache do navegador
- ✅ Verifique JavaScript habilitado
- ✅ Inspecione erros no console

---

**Bons testes! 🎟️📚**
