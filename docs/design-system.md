# Design System

O projeto usa **TailwindCSS** (via CDN no desenvolvimento) com **Django Template Language**.
Fonte: **Inter** via Google Fonts.

```html
<!-- Adicionar no <head> do base.html -->
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style> body { font-family: 'Inter', sans-serif; } </style>
```

---

## Paleta de cores

| Papel | Classe Tailwind | Hex |
|---|---|---|
| Primária (verde) | `bg-emerald-600` | `#059669` |
| Primária hover | `bg-emerald-700` | `#047857` |
| Primária clara | `bg-emerald-50` | `#ECFDF5` |
| Gradiente hero | `from-emerald-600 to-teal-500` | — |
| Fundo principal | `bg-gray-50` | `#F9FAFB` |
| Fundo de card | `bg-white` | `#FFFFFF` |
| Texto principal | `text-gray-800` | `#1F2937` |
| Texto secundário | `text-gray-500` | `#6B7280` |
| Borda | `border-gray-200` | `#E5E7EB` |
| Receita | `text-emerald-600` | `#059669` |
| Despesa | `text-red-500` | `#EF4444` |
| Alerta | `text-yellow-500` | `#F59E0B` |

---

## Tipografia

```html
<!-- Título de página -->
<h1 class="text-2xl font-bold text-gray-800">Contas Bancárias</h1>

<!-- Subtítulo de seção -->
<h2 class="text-lg font-semibold text-gray-700">Resumo</h2>

<!-- Texto de corpo -->
<p class="text-sm text-gray-600">Descrição</p>

<!-- Label de formulário -->
<label class="block text-sm font-medium text-gray-700">Nome da conta</label>

<!-- Texto secundário / metadado -->
<span class="text-xs text-gray-400">12/03/2026</span>
```

---

## Botões

```html
<!-- Primário -->
<button class="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700
               text-white text-sm font-medium rounded-lg transition-colors duration-200
               focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2">
  Salvar
</button>

<!-- Secundário (outline) -->
<button class="inline-flex items-center px-4 py-2 border border-gray-300
               bg-white hover:bg-gray-50 text-gray-700 text-sm font-medium
               rounded-lg transition-colors duration-200">
  Cancelar
</button>

<!-- Perigo (exclusão) -->
<button class="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700
               text-white text-sm font-medium rounded-lg transition-colors duration-200">
  Excluir
</button>

<!-- Pequeno (ação em tabela) -->
<a href="#" class="px-3 py-1 text-xs font-medium text-emerald-700 bg-emerald-50
                   hover:bg-emerald-100 rounded-md transition-colors duration-150">
  Editar
</a>
```

---

## Inputs e formulários

```html
<!-- Input de texto -->
<input type="text"
       class="block w-full px-3 py-2 border border-gray-300 rounded-lg
              text-sm text-gray-800 placeholder-gray-400
              focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500
              transition-colors duration-200">

<!-- Select -->
<select class="block w-full px-3 py-2 border border-gray-300 rounded-lg
               text-sm text-gray-800 bg-white
               focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
  <option>Opção</option>
</select>

<!-- Input de data -->
<input type="date"
       class="block w-full px-3 py-2 border border-gray-300 rounded-lg
              text-sm text-gray-800
              focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">

<!-- Textarea -->
<textarea rows="3"
          class="block w-full px-3 py-2 border border-gray-300 rounded-lg
                 text-sm text-gray-800 placeholder-gray-400 resize-none
                 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
</textarea>

<!-- Grupo de campo com label e erro -->
<div>
  <label class="block text-sm font-medium text-gray-700 mb-1">Campo</label>
  <input type="text" class="...input classes...">
  {% if form.field.errors %}
    <p class="mt-1 text-xs text-red-500">{{ form.field.errors.0 }}</p>
  {% endif %}
</div>

<!-- Card de formulário -->
<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
  <h2 class="text-lg font-semibold text-gray-800 mb-6">Nova Conta</h2>
  <form method="post">
    {% csrf_token %}
    <div class="space-y-4">
      <!-- campos -->
    </div>
    <div class="flex gap-3 mt-6">
      <button type="submit" class="...botão primário...">Salvar</button>
      <a href="{% url 'accounts:list' %}" class="...botão secundário...">Cancelar</a>
    </div>
  </form>
</div>
```

---

## Cards de métricas (dashboard)

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

  <!-- Saldo total -->
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-500">Saldo Total</p>
        <p class="text-2xl font-bold text-gray-800">R$ 0,00</p>
      </div>
      <div class="p-3 bg-emerald-50 rounded-lg">
        <!-- ícone SVG -->
      </div>
    </div>
  </div>

  <!-- Receitas do mês -->
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-500">Receitas do Mês</p>
        <p class="text-2xl font-bold text-emerald-600">R$ 0,00</p>
      </div>
      <div class="p-3 bg-emerald-50 rounded-lg">
        <!-- ícone SVG -->
      </div>
    </div>
  </div>

  <!-- Despesas do mês -->
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-500">Despesas do Mês</p>
        <p class="text-2xl font-bold text-red-500">R$ 0,00</p>
      </div>
      <div class="p-3 bg-red-50 rounded-lg">
        <!-- ícone SVG -->
      </div>
    </div>
  </div>

</div>
```

---

## Tabelas

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
  <table class="w-full text-sm">
    <thead class="bg-gray-50 border-b border-gray-200">
      <tr>
        <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Descrição
        </th>
        <th class="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Valor
        </th>
        <th class="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          Ações
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-100">
      {% for item in object_list %}
      <tr class="hover:bg-gray-50 transition-colors duration-150">
        <td class="px-6 py-4 text-gray-700">{{ item.name }}</td>
        <td class="px-6 py-4
                   {% if item.transaction_type == 'income' %}text-emerald-600{% else %}text-red-500{% endif %}
                   font-medium">
          R$ {{ item.amount }}
        </td>
        <td class="px-6 py-4 text-right space-x-2">
          <a href="{% url 'app:update' item.pk %}" class="...botão pequeno...">Editar</a>
          <a href="{% url 'app:delete' item.pk %}" class="...botão perigo pequeno...">Excluir</a>
        </td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="3" class="px-6 py-8 text-center text-sm text-gray-400">
          Nenhum registro encontrado.
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

---

## Mensagens de feedback (Django Messages)

```html
{% if messages %}
  <div class="space-y-2 mb-4">
    {% for message in messages %}
      <div class="px-4 py-3 rounded-lg text-sm font-medium
                  {% if message.tags == 'success' %}bg-emerald-50 text-emerald-700 border border-emerald-200
                  {% elif message.tags == 'error' %}bg-red-50 text-red-700 border border-red-200
                  {% else %}bg-blue-50 text-blue-700 border border-blue-200{% endif %}">
        {{ message }}
      </div>
    {% endfor %}
  </div>
{% endif %}
```

---

## Sidebar (área autenticada)

```html
<aside class="w-64 bg-white border-r border-gray-200 min-h-screen flex flex-col">

  <!-- Logo -->
  <div class="px-6 py-5 border-b border-gray-200">
    <span class="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-500
                 bg-clip-text text-transparent">my-denarius</span>
  </div>

  <!-- Navegação -->
  <nav class="flex-1 px-4 py-4 space-y-1">
    <a href="{% url 'dashboard' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium
              {% if request.resolver_match.url_name == 'dashboard' %}
                bg-emerald-50 text-emerald-700
              {% else %}
                text-gray-600 hover:bg-emerald-50 hover:text-emerald-700
              {% endif %}
              transition-colors duration-200">
      <!-- ícone --> Dashboard
    </a>
    <!-- repetir para: Contas, Categorias, Transações, Perfil -->
  </nav>

  <!-- Logout -->
  <div class="px-4 py-4 border-t border-gray-200">
    <a href="{% url 'logout' %}"
       class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium
              text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors duration-200">
      Sair
    </a>
  </div>

</aside>
```

---

## Navbar pública

```html
<nav class="bg-white border-b border-gray-200 px-6 py-4">
  <div class="max-w-6xl mx-auto flex items-center justify-between">
    <span class="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-500
                 bg-clip-text text-transparent">my-denarius</span>
    <div class="flex gap-3">
      <a href="{% url 'login' %}"
         class="inline-flex items-center px-4 py-2 border border-gray-300
                bg-white hover:bg-gray-50 text-gray-700 text-sm font-medium
                rounded-lg transition-colors duration-200">
        Entrar
      </a>
      <a href="{% url 'register' %}"
         class="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700
                text-white text-sm font-medium rounded-lg transition-colors duration-200">
        Cadastre-se
      </a>
    </div>
  </div>
</nav>
```

---

## Hero (página pública)

```html
<section class="bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-400 text-white py-24">
  <div class="max-w-4xl mx-auto text-center px-6">
    <h1 class="text-5xl font-bold mb-4">Controle suas finanças<br>com simplicidade</h1>
    <p class="text-emerald-100 text-lg mb-8">
      Registre receitas e despesas, organize por categorias e acompanhe seu saldo.
    </p>
    <a href="{% url 'register' %}"
       class="bg-white text-emerald-700 font-semibold px-8 py-3 rounded-lg
              hover:bg-emerald-50 transition-colors duration-200">
      Começar gratuitamente
    </a>
  </div>
</section>
```

---

## Página de confirmação de exclusão

```html
<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 max-w-md mx-auto mt-10">
  <h2 class="text-lg font-semibold text-gray-800 mb-2">Confirmar exclusão</h2>
  <p class="text-sm text-gray-600 mb-6">
    Tem certeza que deseja excluir <strong>{{ object }}</strong>? Esta ação não pode ser desfeita.
  </p>
  <form method="post">
    {% csrf_token %}
    <div class="flex gap-3">
      <button type="submit"
              class="inline-flex items-center px-4 py-2 bg-red-600 hover:bg-red-700
                     text-white text-sm font-medium rounded-lg transition-colors duration-200">
        Excluir
      </button>
      <a href="{{ request.META.HTTP_REFERER }}"
         class="inline-flex items-center px-4 py-2 border border-gray-300
                bg-white hover:bg-gray-50 text-gray-700 text-sm font-medium
                rounded-lg transition-colors duration-200">
        Cancelar
      </a>
    </div>
  </form>
</div>
```
