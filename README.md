# 📊 Dashboard — Evaluación Anual de Indicadores 2025

**Universidad Católica de Temuco — Sistema Integrado de Aseguramiento de la Calidad (SIAC)**

Dashboard interactivo construido con [Streamlit](https://streamlit.io) que visualiza los indicadores de calidad de la UCT correspondientes al año 2025, basado en el documento **SGC PS-FOR-PS 0042 v01**.

## 🎯 Indicadores del SGC

| Indicador | Descripción | Meta |
|-----------|-------------|------|
| **IND-PS-0001** | Eficacia de Acciones Correctivas (No Conformidades) | ≥ 75% |
| **IND-PS-0003** | Cumplimiento de Requisitos Legales | 100% |
| **IND-PS-0004** | Satisfacción del Usuario (Procesos de Soporte) | ≥ 89% |
| **IND-PS-0005** | Quejas del Usuario | ≤ 1 respondida |
| **IND-PS-0006** | Desempeño Operacional (varios sub-indicadores) | Variable |

## 🚀 Ejecutar localmente

```bash
# Clonar el repositorio
git clone https://github.com/USUARIO/uct-calidad-2025.git
cd uct-calidad-2025

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
streamlit run app.py
```

## 📁 Estructura

```
├── app.py              # Código principal del dashboard
├── requirements.txt    # Dependencias Python
├── data/
│   └── indicadores.xlsx  # Fuente de datos (Excel)
├── README.md
└── .gitignore
```

## 📋 Fuente de datos

Los datos provienen del archivo Excel **"Evaluación Anual de Indicadores 2025"** proporcionado por la Oficina de Calidad de la UCT. El dashboard carga los datos en tiempo real desde el archivo Excel.

> **Nota:** Algunos indicadores pueden tener datos parciales dependiendo de la etapa del proceso de evaluación.

## 🎨 Diseño

Paleta **Open Design** — colores claros, tipografía Inter, sombras sutiles y bordes limpios para una experiencia de visualización accesible y profesional.

## 📄 Licencia

MIT — Universidad Católica de Temuco
