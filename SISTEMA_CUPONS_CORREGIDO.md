# 🎟️ Sistema de Cupons de Desconto - CORREGIDO

## ✅ Sistema PROFESIONAL Implementado

### 🔒 Características CORRECTAS del Sistema

#### **1. CUPONES SECRETOS**
- ❌ **ELIMINADA** página pública `/cupons/` 
- ✅ Los códigos son **SECRETOS**
- ✅ Solo visibles en el **panel de administración**
- ✅ Solo los **administradores** pueden verlos y crearlos

#### **2. UN SOLO USO**
- ✅ **Cada cupón = 1 uso ÚNICO**
- ✅ `uso_maximo = 1`
- ✅ `uso_por_utilizador = 1`
- ✅ Una vez usado → Se marca como "USADO" automáticamente
- ✅ **FORZADO** en el código: El admin no puede modificar esto

---

## 📡 ¿Qué es AJAX y por qué se usa aquí?

### Explicación Simple de AJAX

**AJAX** = **A**synchronous **J**avaScript **A**nd **X**ML

**¿Qué hace?**
- Permite **comunicación con el servidor SIN recargar la página**
- Es como enviar un mensaje y recibir respuesta mientras sigues trabajando

### Comparación Visual

**❌ SIN AJAX (Método antiguo)**:
```
Usuario escribe cupón "OUTONO2025"
    ↓
Clic en "Aplicar"
    ↓
⏳ TODA la página se RECARGA (pierdes formulario, scroll, etc.)
    ↓
Servidor valida
    ↓
Página nueva muestra si es válido
```

**✅ CON AJAX (Método moderno)**:
```
Usuario escribe cupón "OUTONO2025"
    ↓
Clic en "Aplicar"
    ↓
⚡ JavaScript envía petición al servidor (en segundo plano)
    ↓
Usuario sigue viendo su formulario intacto
    ↓
Servidor responde (válido/inválido)
    ↓
JavaScript actualiza SOLO la parte del descuento
    ↓
✨ Experiencia rápida, sin perder información
```

### ¿Cuándo se usa AJAX?

#### ✅ **Usos Comunes**:
1. **Validaciones en tiempo real**
   - Cupones (como en tu caso)
   - Verificar si username está disponible
   - Validar email mientras escribes

2. **Búsquedas instantáneas**
   - Google Search (sugerencias)
   - Autocompletado de direcciones
   - Filtros de productos

3. **Actualizar datos sin recargar**
   - Carritos de compra
   - Notificaciones en vivo
   - Chat/mensajería

4. **Cargar contenido dinámico**
   - Scroll infinito (Instagram, Facebook)
   - Comentarios sin recargar
   - "Cargar más productos"

5. **Formularios inteligentes**
   - Guardar borrador automático
   - Calcular precios en vivo
   - Verificar disponibilidad

#### ❌ **Cuándo NO usar AJAX**:
- Cambiar de página completa → Usa link normal
- Formularios simples sin validación → POST tradicional
- Descargar archivos → Link directo

### En tu Sistema de Cupones

**¿Por qué AJAX aquí?**
```javascript
// Usuario en checkout con formulario LLENO:
// - Nombre: Manuel Silva
// - Dirección: Rua das Flores, 123
// - Email: manuel@email.com
// - Teléfono: +351 21 XXX XXXX
// - Carrito: 3 libros (€45.00)

// Usuario escribe cupón: OUTONO2025
// Clic en "Aplicar"

// ❌ SIN AJAX:
// → Página recarga
// → Pierde TODOS los datos del formulario
// → Tiene que rellenar todo de nuevo
// → MALA experiencia

// ✅ CON AJAX:
fetch('/validar-cupom/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.valido) {
        // ✅ Cupón válido
        // → Actualiza SOLO el descuento
        // → Formulario intacto
        // → Usuario feliz
        mostrarDescuento(data.desconto);
    } else {
        // ❌ Cupón inválido
        mostrarError(data.erro);
    }
});
```

---

## 🎯 Cómo Funciona el Sistema CORREGIDO

### Flujo Completo

1. **Creación de Cupón (Solo Admin)**
   ```
   Admin → Panel Admin → Cupons → Añadir Cupom
   Código: ESPECIAL50
   Descuento: 50%
   Mínimo: €30
   Válido hasta: 31/12/2025
   ```
   → Sistema **FUERZA** automáticamente: `uso_maximo = 1`

2. **Distribución del Código (Manual)**
   ```
   Admin copia el código: ESPECIAL50
   Envía por:
   - Email personal al cliente
   - Newsletter
   - Redes sociales
   - Promoción en tienda física
   ```

3. **Uso por Cliente**
   ```
   Cliente en checkout
   Ve campo: "Tens um cupom?"
   Escribe: ESPECIAL50
   Clic "Aplicar"
   ```

4. **Validación AJAX**
   ```javascript
   JavaScript → POST /validar-cupom/
   {
     codigo: "ESPECIAL50",
     valor_pedido: 45.00
   }
   
   Servidor valida:
   ✅ ¿Código existe? Sí
   ✅ ¿Está activo? Sí
   ✅ ¿Está vigente? Sí (dentro de fechas)
   ✅ ¿Ya fue usado? No
   ✅ ¿Valor mínimo cumplido? Sí (€45 > €30)
   
   Respuesta:
   {
     valido: true,
     desconto: 22.50,  // 50% de 45
     descricao: "50% de desconto"
   }
   ```

5. **Aplicación del Descuento**
   ```
   JavaScript actualiza la página SIN recargar:
   
   Subtotal:     €45.00
   IVA (23%):    €10.35
   Descuento:   -€22.50  ← NUEVO
   ────────────────────
   TOTAL:        €32.85
   
   ✅ Cupón ESPECIAL50 aplicado
   ```

6. **Finalizar Pedido**
   ```
   Cliente confirma pedido
   
   Sistema:
   1. Crea el pedido con descuento
   2. Marca cupom.vezes_usado = 1
   3. Crea registro UsoCupom
   4. Estado cambia a "USADO"
   5. ❌ NADIE MÁS puede usar ESPECIAL50
   ```

---

## 🔐 Seguridad Implementada

### 1. **Cupones Secretos**
```python
# ❌ ELIMINADO: Vista pública
# def lista_cupons(request):
#     return render(...)

# ❌ ELIMINADO: URL pública
# path('cupons/', views.lista_cupons)

# ✅ Solo en Admin (requiere login de staff)
@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    # Solo accesible por is_staff=True
```

### 2. **Uso Único Forzado**
```python
def save_model(self, request, obj, form, change):
    # FORZAR que SIEMPRE sea de un solo uso
    obj.uso_maximo = 1
    obj.uso_por_utilizador = 1
    super().save_model(request, obj, form, change)
```

### 3. **Validación Completa**
```python
@login_required
def validar_cupom(request):
    # 1. Usuario autenticado
    # 2. Código existe
    # 3. Está activo
    # 4. Fecha válida
    # 5. No usado aún
    # 6. Valor mínimo cumplido
    # 7. Usuario puede usarlo
```

---

## 🎟️ Cupones de Prueba (SECRETOS)

**⚠️ IMPORTANTE**: Estos códigos NO deben mostrarse públicamente

### Códigos Disponibles (Solo para Admin/Testing):

1. **OUTONO2025** - 10% descuento, mín €20
2. **NATAL2025** - 15% descuento, mín €30
3. **BLACKFRIDAY2025** - 20% descuento, sin mínimo
4. **VIP25** - 25% descuento, mín €40
5. **BEMVINDO5** - €5 descuento, mín €15
6. **GRANDE10** - €10 descuento, mín €50

**Cada código = 1 USO ÚNICO**

---

## 📊 Panel de Administración

### Ver Cupones
```
http://127.0.0.1:8000/admin/members/cupom/

Lista muestra:
- Código (secreto)
- Tipo (% o €)
- Valor
- Periodo de validade
- Status (✓ Válido / ✗ Inválido)
- Estado de Uso (✓ DISPONIBLE / ✗ USADO)
```

### Crear Nuevo Cupón
```
1. Clic "Añadir Cupom"
2. Código: VERANO2026 (única, mayúsculas)
3. Descripción: Promoción de verano
4. Tipo: Percentagem
5. Valor: 30
6. Mínimo: €50.00
7. Inicio: 01/06/2026
8. Fin: 30/09/2026
9. Guardar

→ Sistema automáticamente:
   uso_maximo = 1
   uso_por_utilizador = 1
```

### Historial de Uso
```
Cada cupón muestra:
- Quién lo usó
- Cuándo
- En qué pedido
- Cuánto ahorró

Inline: UsoCupom
- Utilizador: manuel_silva
- Pedido: #1234
- Descuento: €15.00
- Data: 06/11/2025 22:15
```

---

## 🧪 Testing

### Test 1: Aplicar Cupón Válido
```
1. Añadir libros al carrito (total > €20)
2. Ir a checkout
3. Escribir: OUTONO2025
4. Clic "Aplicar"
5. ✅ Debe mostrar: "10% de descuento"
6. ✅ Total debe reducirse
```

### Test 2: Cupón Ya Usado
```
1. Usar OUTONO2025 en un pedido
2. Intentar usar OUTONO2025 de nuevo
3. ❌ Debe mostrar: "Este cupom atingiu o limite de utilizações"
```

### Test 3: Valor Mínimo No Cumplido
```
1. Carrito con €15 (menos de €20)
2. Escribir: OUTONO2025
3. ❌ Debe mostrar: "Valor mínimo do pedido: €20.00"
```

### Test 4: Código Inválido
```
1. Escribir: CUPOMINEXISTENTE
2. ❌ Debe mostrar: "Cupom inválido ou não encontrado"
```

### Test 5: Cupón Expirado
```
(Esperar fecha de fin o modificar en admin)
❌ Debe mostrar: "Este cupom expirou"
```

---

## 📝 Resumen de Cambios

### ❌ ELIMINADO:
- Vista `lista_cupons()` que mostraba cupones públicamente
- URL `/cupons/` pública
- Link "🎟️ Cupons" en navegación
- Template `lista_cupons.html`
- Campos editables `uso_maximo` y `uso_por_utilizador` en admin

### ✅ AGREGADO/CORREGIDO:
- Forzar `uso_maximo = 1` en `save_model()`
- Forzar `uso_por_utilizador = 1` en `save_model()`
- Campos readonly en admin para evitar modificación
- Columna "Estado de Uso" (DISPONIBLE/USADO)
- Advertencia en admin: "⚠️ USO ÚNICO - AUTOMÁTICO"
- Script actualización: todos cupones → 1 uso

### 🔒 MANTENIDO (Correcto):
- Validación AJAX en tiempo real
- Sistema de tracking con UsoCupom
- Admin interface con estadísticas
- Integración en checkout
- Cálculo automático de descuento

---

## 🎓 Lección Aprendida

**Error Original**: Pensé en un sistema tipo "Amazon Prime Day" donde muchos usan el mismo cupón

**Realidad Profesional**: 
- Los cupones son como **billetes de lotería** → únicos
- Se distribuyen **manualmente** por email/newsletter
- Cada cliente recibe **su código exclusivo**
- Esto previene **fraude** y **abuso**
- Permite **tracking preciso** de marketing

**Analogía Real**:
```
❌ MAL: Cupón "VERANO50" → 1000 personas pueden usar
     → No sabes quién lo compartió
     → Pérdidas incontroladas

✅ BIEN: Cupones únicos por persona:
     VERANO-MANUEL-2025
     VERANO-JOAO-2025  
     VERANO-MARIA-2025
     → Cada uno = 1 uso
     → Sabes exactamente quién compró
     → Control total de descuentos
```

---

## 🚀 Sistema Listo para Producción

El sistema ahora es **100% profesional** y sigue las mejores prácticas de la industria:

✅ Cupones secretos (solo admins)
✅ Uso único (anti-fraude)
✅ Validación AJAX (UX moderna)
✅ Tracking completo (analytics)
✅ Seguridad robusta (validaciones)
✅ Admin interface intuitiva

**Desarrollado con**: Django 5.2.6, JavaScript AJAX, PostgreSQL-ready
**Fecha**: Noviembre 2025
**Proyecto**: Cantos de Papel - Sistema E-commerce Profesional

---

**¡Ahora sí es un sistema REAL de cupones! 🎉**
