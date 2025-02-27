import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import optuna
from statsmodels.tsa.arima.model import ARIMA
from report_generator import create_pdf_report

def generate_time_series_analysis(filepath, static_folder, report_folder):
    """ Genera análisis de series de tiempo y gráficos optimizados con Optuna """
    df = pd.read_excel(filepath)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df = df.sort_values(by='fecha')
    
    sns.set_style("darkgrid")
    palette = sns.color_palette("husl")
    
    # 📈 1. Gráfico de Serie de Tiempo
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='fecha', y='total', marker='o', linestyle='-', color=palette[0])
    plt.title("📈 Evolución de Ventas en el Tiempo", fontsize=14, fontweight='bold')
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Total de Ventas", fontsize=12)
    plt.xticks(rotation=45)
    series_tiempo_path = os.path.join(static_folder, "series_tiempo.png")
    plt.savefig(series_tiempo_path, dpi=300)
    plt.close()
    
    # 📊 2. Descomposición de la Serie de Tiempo
    descomposicion = sm.tsa.seasonal_decompose(df.set_index('fecha')['total'], model='additive', period=7)
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    descomposicion.trend.plot(ax=axes[0], title="📊 Tendencia", color=palette[1])
    descomposicion.seasonal.plot(ax=axes[1], title="🔄 Estacionalidad", color=palette[2])
    descomposicion.resid.plot(ax=axes[2], title="📉 Residuales", color=palette[3])
    descomposicion_path = os.path.join(static_folder, "descomposicion_tiempo.png")
    plt.savefig(descomposicion_path, dpi=300)
    plt.close()
    
    # 🔮 Optimización con Optuna para ARIMA
    def objective(trial):
        p = trial.suggest_int('p', 0, 5)
        d = trial.suggest_int('d', 0, 2)
        q = trial.suggest_int('q', 0, 5)
        model = ARIMA(df['total'], order=(p, d, q)).fit()
        return model.aic
    
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=10)
    best_params = study.best_params
    
    # 📊 Predicción con ARIMA optimizado
    best_model = ARIMA(df['total'], order=(best_params['p'], best_params['d'], best_params['q'])).fit()
    forecast = best_model.forecast(steps=10)
    forecast_index = pd.date_range(start=df['fecha'].iloc[-1], periods=11, freq='D')[1:]
    
    plt.figure(figsize=(10, 5))
    plt.plot(df['fecha'], df['total'], label="Ventas Reales", marker='o', color=palette[4])
    plt.plot(forecast_index, forecast, label="Pronóstico", linestyle='--', color=palette[5])
    plt.title("🔮 Pronóstico de Ventas", fontsize=14, fontweight='bold')
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Total de Ventas", fontsize=12)
    plt.legend()
    pronostico_path = os.path.join(static_folder, "pronostico.png")
    plt.savefig(pronostico_path, dpi=300)
    plt.close()
    
    # 📄 Generar informe en PDF
    resumen = {
        'total_ventas': df['total'].sum(),
        'mejor_modelo': best_params
    }
    pdf_filename = create_pdf_report(df, report_folder, ["series_tiempo.png", "descomposicion_tiempo.png", "pronostico.png"], resumen)
    
    return {"series_tiempo": "series_tiempo.png", "descomposicion": "descomposicion_tiempo.png", "pronostico": "pronostico.png"}, resumen, pdf_filename