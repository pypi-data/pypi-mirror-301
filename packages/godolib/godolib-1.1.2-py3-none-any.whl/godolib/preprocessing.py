import pandas as pd
from .testers import StationarityTester
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

class TimeSeriesMonitor ():
    def __init__ (self, df, fit_mode='all_positive'):
        self.df = df
        plt.style.use('dark_background')
        roc_calculator = ROCCalculator(fit_mode=fit_mode)
        returns_df = roc_calculator.fit_transform(df)
        self.returns_df = returns_df
    def describe_statistics (self, returns = False):
        df = self.returns_df if returns else self.df
        return df.describe()
    def calculate_skewness_kurtosis (self, returns = False):
        df = self.returns_df if returns else self.df
        skewness = df.skew()
        kurtosis = df.kurt()
        result = pd.DataFrame({
            'Skewness' : skewness,
            'Kurtosis' : kurtosis
        })
        return result
    def calculate_dispersion_measures (self, returns = False):
        df = self.returns_df if returns else self.df
        variance = df.var()
        iqr = df.quantile(0.75) - df.quantile(0.25)  # IQR = Q3 - Q1
        result = pd.DataFrame({
            'Variance': variance,
            'IQR': iqr
        })
        return result
    def plot_descriptive_statistics(self, returns=False, backend='matplotlib'):
        """
        Grafica las estadísticas descriptivas de las series temporales.
    
        Parameters:
            returns (bool): Si se usa el DataFrame de retornos o los datos originales.
            backend (str): El motor de gráficos a usar ('matplotlib' o 'plotly').
        """
        df = self.returns_df if returns else self.df
        desc_stats = df.describe().T
        skew_kurtosis = self.calculate_skewness_kurtosis(returns=returns)
        dispersion = self.calculate_dispersion_measures(returns=returns)
    
        titles = ['Mean', 'Variance', 'Skewness', 'Kurtosis']
        data = [
            desc_stats['mean'], 
            dispersion['Variance'], 
            skew_kurtosis['Skewness'], 
            skew_kurtosis['Kurtosis']
        ]
        colors = ['cyan', 'magenta', 'yellow', 'orange']
        y_labels = ['Value', 'Value', 'Skewness', 'Kurtosis']
    
        if backend == 'matplotlib':

            fig, axs = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle('Descriptive Statistics of Time Series', fontsize=16)
    
            for i, ax in enumerate(axs.flat):
                ax.bar(df.columns, data[i], color=colors[i], edgecolor='white')
                ax.set_title(titles[i])
                ax.set_ylabel(y_labels[i])
                ax.set_xticks(range(len(df.columns)))
                ax.set_xticklabels(df.columns, rotation=45, ha='right')
                ax.grid(True, color='gray', linestyle='--')
                if titles[i] in ['Skewness', 'Kurtosis']:
                    ax.axhline(0, color='red', linestyle='--', lw=1)
    
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()
    
        elif backend == 'plotly':
            # Graficar usando plotly

    
            # Crear subplots en una cuadrícula de 2x2
            fig = make_subplots(rows=2, cols=2, subplot_titles=titles)
    
            # Añadir los gráficos de barras para cada estadística
            for i, (stat_data, color, y_label, title) in enumerate(zip(data, colors, y_labels, titles)):
                row = i // 2 + 1
                col = i % 2 + 1
                fig.add_trace(go.Bar(
                    x=df.columns,
                    y=stat_data,
                    marker=dict(color=color),
                    name=title
                ), row=row, col=col)
                
                # Configuración de la línea horizontal en Skewness y Kurtosis
                if title in ['Skewness', 'Kurtosis']:
                    fig.add_hline(y=0, line=dict(color='red', dash='dash'), row=row, col=col)
    
                # Actualizar ejes
                fig.update_yaxes(title_text=y_label, row=row, col=col)
                fig.update_xaxes(tickangle=45, title_text='Features', row=row, col=col)
    
            # Configuración general del layout
            fig.update_layout(
                title='Descriptive Statistics of Time Series',
                width=1000,  # Ancho de la figura
                height=800,  # Alto de la figura
                template='plotly_dark',
                showlegend=False
            )
    
            fig.show()
    
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def plot_time_series(self, feature, returns=False, backend='matplotlib'):
        """
        Grafica una serie temporal.
    
        Parameters:
            feature (str): El nombre de la característica a analizar.
            returns (bool): Si se usa el DataFrame de retornos o los datos originales.
            backend (str): El motor de gráficos a usar ('matplotlib' o 'plotly').
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        mean_value = time_series.mean()
    
        if backend == 'matplotlib':
            # Graficar usando matplotlib

            plt.figure(figsize=(12, 6), facecolor='black')
            plt.plot(time_series, color='blue', label=time_series.name)
            plt.axhline(mean_value, color='red', linestyle='--', label=f'Media: {mean_value:.4f}')
            plt.title(f'Serie Temporal: {feature_name}')
            plt.xlabel('Índice')
            plt.ylabel('Valor')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            # Graficar usando plotly

    
            # Serie temporal
            time_series_trace = go.Scatter(
                x=time_series.index,
                y=time_series,
                mode='lines',
                line=dict(color='blue'),
                name=f'Serie Temporal: {feature_name}'
            )
    
            # Línea de la media
            mean_line = go.Scatter(
                x=[time_series.index.min(), time_series.index.max()],
                y=[mean_value, mean_value],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name=f'Media: {mean_value:.4f}'
            )
    
            # Crear la figura
            fig = go.Figure(data=[time_series_trace, mean_line])
    
            # Configuración de la figura
            fig.update_layout(
                title=f'Serie Temporal: {feature_name}',
                xaxis_title='Índice',
                yaxis_title='Valor',
                width=1000,  # Ancho de la figura
                height=600,  # Alto de la figura
                template='plotly_dark',
                hovermode='x unified'
            )
    
            fig.show()
    
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def plot_distribution(self, feature, returns=False, backend='matplotlib'):
        """
        Grafica la distribución de una serie temporal.
    
        Parameters:
            feature (str): El nombre de la característica a analizar.
            returns (bool): Si se usa el DataFrame de retornos o los datos originales.
            backend (str): El motor de gráficos a usar ('matplotlib' o 'plotly').
        """

        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        mean_value = np.mean(time_series)
    
        if backend == 'matplotlib':

            plt.figure(figsize=(10, 6))
            plt.hist(time_series, bins=30, alpha=0.7, color='blue', edgecolor='black', density=True)
            plt.axvline(mean_value, color='red', linestyle='--', label=f'Media: {mean_value:.4f}')
            plt.title(f'{feature_name} Distribution')
            plt.xlabel('Valor')
            plt.ylabel('Densidad')
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            # Graficar usando plotly
    
            # Histograma con plotly
            hist_data = go.Histogram(
                x=time_series,
                nbinsx=30,
                histnorm='probability density',
                marker=dict(color='blue', line=dict(color='black', width=1)),
                opacity=0.7,
                name='Distribución'
            )
    
            # Línea de la media
            mean_line = go.Scatter(
                x=[mean_value, mean_value],
                y=[0, max(np.histogram(time_series, bins=30, density=True)[0])],
                mode='lines',
                line=dict(color='red', dash='dash'),
                name=f'Media: {mean_value:.4f}'
            )
    
            # Crear la figura
            fig = go.Figure(data=[hist_data, mean_line])
    
            # Configuración de la figura
            fig.update_layout(
                title=f'{feature_name} Distribution',
                xaxis_title='Valor',
                yaxis_title='Densidad',
                width=1000,  # Ancho de la figura
                height=600,  # Alto de la figura
                template='plotly_dark',
                hovermode='x unified'
            )
    
            # Ajustar el rango del eje Y para mejorar la visualización
            fig.update_yaxes(range=[0, max(np.histogram(time_series, bins=30, density=True)[0]) * 1.1])
    
            fig.show()
    
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def get_feature_autoc (self, feature, lags = 40, returns = False):
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        acf_values = acf(time_series, nlags = lags)
        pacf_values = pacf(time_series, nlags = lags)
        df = pd.DataFrame([acf_values, pacf_values]).T
        df.columns = ['ACF', 'PACF']
        df.index = [f'lag {i}' for i in range (lags + 1)]
        return df
    def get_significant_lags (self, top=5, func='ACF', scorer = 'mean', lags = 40, returns = False):
        df = self.returns_df if returns else self.df
        valid_scorers = ['mean', 'sum']
        valid_funcs = ['ACF', 'PACF']
        if func not in valid_funcs:
            raise ValueError(f"'{func}' is not a valid mode. Choose from {valid_funcs}.")
        if scorer not in valid_scorers:
            raise ValueError(f"'{scorer}' is not a valid mode. Choose from {valid_scorers}.")
        func_dict = {}
        for feature in df:
            current_func_results = self.get_feature_autoc(feature, lags, returns = returns)[func].values
            func_dict[feature] = current_func_results
        func_df = pd.DataFrame(func_dict, index=[f'lag {i}' for i in range (lags + 1)])
        if scorer == 'mean':
            func_df[scorer] = func_df.mean(axis = 1)
        elif scorer == 'sum':
            func_df[scorer] = func_df.sum(axis = 1)
        top_rows = func_df.nlargest(top, scorer)#.drop(columns=scorer)
        return top_rows
        
    def plot_acf_pacf(self, feature, lags=40, returns=False, backend='matplotlib'):

        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
    
        if backend == 'matplotlib':
            # Graficar usando matplotlib
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(2, 1, figsize=(12, 8), facecolor='black')
    
            plot_acf(time_series, lags=lags, ax=ax[0])
            ax[0].set_title(f'Autocorrelation Function (ACF) for {feature_name}', color='white')
            ax[0].set_facecolor('black')
            ax[0].grid(True, color='gray', linestyle='--')
            ax[0].tick_params(axis='x', colors='white')
            ax[0].tick_params(axis='y', colors='white')
    
            plot_pacf(time_series, lags=lags, ax=ax[1])
            ax[1].set_title(f'Partial Autocorrelation Function (PACF) for {feature_name}', color='white')
            ax[1].set_facecolor('black')
            ax[1].grid(True, color='gray', linestyle='--')
            ax[1].tick_params(axis='x', colors='white')
            ax[1].tick_params(axis='y', colors='white')
    
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            # Graficar usando plotly
    
            # Calcular los valores de ACF y PACF
            acf_values = acf(time_series, nlags=lags)
            pacf_values = pacf(time_series, nlags=lags)
    
            # Crear la figura de Plotly
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(
                f'Autocorrelation Function (ACF) for {feature_name}', 
                f'Partial Autocorrelation Function (PACF) for {feature_name}'
            ))
    
            # ACF
            fig.add_trace(go.Bar(
                x=list(range(len(acf_values))),
                y=acf_values,
                name='ACF',
                marker=dict(color='cyan')
            ), row=1, col=1)
    
            # PACF
            fig.add_trace(go.Bar(
                x=list(range(len(pacf_values))),
                y=pacf_values,
                name='PACF',
                marker=dict(color='magenta')
            ), row=2, col=1)
    
            # Configuración de la figura
            fig.update_layout(
                height=800,  # Alto de la figura
                width=1200,  # Ancho de la figura
                template='plotly_dark',
                showlegend=False,
                title_text=f'ACF and PACF for {feature_name}',
                hovermode='x unified'
            )
    
            # Etiquetas de los ejes
            fig.update_xaxes(title_text='Lags', row=2, col=1)
            fig.update_yaxes(title_text='Correlation', row=1, col=1)
            fig.update_yaxes(title_text='Partial Correlation', row=2, col=1)
    
            fig.show()
    
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    def lag_scatter(self, feature, lag=1, returns=False, backend='matplotlib'):
        
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        t_series = time_series[lag:]
        t_lag_series = time_series[:-lag]
    
        if backend == 'matplotlib':
            # Graficar usando matplotlib
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 6))
            plt.plot(t_series, t_lag_series, 'o')
            plt.xlabel('t series')
            plt.ylabel('t-lag series')
            plt.title(f'Lagged {feature_name} Correlation')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
    
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=t_series, 
                y=t_lag_series, 
                mode='markers', 
                marker=dict(color='blue'),
                name='Lag Scatter'
            ))
    
            # Configuración de la figura para hacerla más grande y habilitar hovermode
            fig.update_layout(
                title=f'Lagged {feature_name} Correlation',
                xaxis_title='t series',
                yaxis_title='t-lag series',
                width=1000,  # Ancho de la figura
                height=600,  # Alto de la figura
                template='plotly_dark',
                hovermode='closest'  # Muestra información más cercana al cursor
            )
    
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    
    def decompose_series (self, feature, model='additive', freq=None, returns = False):
        df = self.returns_df if returns else self.df
        time_series, _ = self._read_feature_(df, feature)
        decomposition = seasonal_decompose(time_series, model=model, period=freq)
        trend, seasonality, residuals = decomposition.trend, decomposition.seasonal, decomposition.resid
        return trend, seasonality, residuals
    def plot_decomposed_series(self, feature, model='additive', freq=None, returns=False, backend='matplotlib'):
        """
        Grafica la serie original y sus componentes descompuestos (tendencia, estacionalidad, residuales).
    
        Parameters:
            feature (str): El nombre de la característica a analizar.
            model (str): Tipo de modelo para la descomposición ('additive' o 'multiplicative').
            freq (int): Frecuencia de la estacionalidad. Si es None, se estima automáticamente.
            returns (bool): Si se usa el DataFrame de retornos o los datos originales.
            backend (str): El motor de gráficos a usar ('matplotlib' o 'plotly').
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        trend, seasonality, residuals = self.decompose_series(feature, model, freq, returns=returns)
    
        if backend == 'matplotlib':
            # Graficar usando matplotlib
            import matplotlib.pyplot as plt
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), facecolor='black')
    
            ax1.plot(time_series, label='Original', color='cyan')
            ax1.set_title(f'Original Series ({feature_name})', color='white')
            ax1.set_facecolor('black')
            ax1.grid(True, color='gray', linestyle='--')
            ax1.tick_params(axis='x', colors='white')
            ax1.tick_params(axis='y', colors='white')
    
            ax2.plot(trend, label='Trend', color='magenta')
            ax2.set_title('Trend', color='white')
            ax2.set_facecolor('black')
            ax2.grid(True, color='gray', linestyle='--')
            ax2.tick_params(axis='x', colors='white')
            ax2.tick_params(axis='y', colors='white')
    
            ax3.plot(seasonality, label='Seasonality', color='yellow')
            ax3.set_title('Seasonality', color='white')
            ax3.set_facecolor('black')
            ax3.grid(True, color='gray', linestyle='--')
            ax3.tick_params(axis='x', colors='white')
            ax3.tick_params(axis='y', colors='white')
    
            ax4.plot(residuals, label='Residuals', color='orange')
            ax4.set_title('Residuals', color='white')
            ax4.set_facecolor('black')
            ax4.grid(True, color='gray', linestyle='--')
            ax4.tick_params(axis='x', colors='white')
            ax4.tick_params(axis='y', colors='white')
    
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            # Graficar usando plotly
    
            # Crear figura con 4 subplots en una columna
            fig = make_subplots(rows=4, cols=1, shared_xaxes=True, subplot_titles=(
                f'Original Series ({feature_name})', 'Trend', 'Seasonality', 'Residuals'))
    
            # Serie original
            fig.add_trace(go.Scatter(x=time_series.index, y=time_series, mode='lines', name='Original', line=dict(color='cyan')), row=1, col=1)
    
            # Tendencia
            fig.add_trace(go.Scatter(x=trend.index, y=trend, mode='lines', name='Trend', line=dict(color='magenta')), row=2, col=1)
    
            # Estacionalidad
            fig.add_trace(go.Scatter(x=seasonality.index, y=seasonality, mode='lines', name='Seasonality', line=dict(color='yellow')), row=3, col=1)
    
            # Residuales
            fig.add_trace(go.Scatter(x=residuals.index, y=residuals, mode='lines', name='Residuals', line=dict(color='orange')), row=4, col=1)
    
            # Configuración de la figura para hacerla más grande y habilitar hovermode
            fig.update_layout(
                height=1000,  # Alto de la figura
                width=1200,   # Ancho de la figura
                template='plotly_dark',
                showlegend=False,
                hovermode='x unified',  # Muestra líneas paralelas a los ejes
                title_text=f'Decomposition of {feature_name} ({model} model)'
            )
    
            # Actualizar diseño de los subplots para que sean más legibles
            fig.update_xaxes(title_text='Tiempo', row=4, col=1)
            fig.update_yaxes(title_text='Valores')
    
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")
    
    def stationarity_test(self, feature, returns = False):
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        adf_result = self._adfuller_(time_series)
        kpss_result = self._kpss_(time_series)
        test_results = {
            'ADF Test': adf_result,
            'KPSS Test': kpss_result
        }
        result = self._clean_stat_result_(test_results)
        return result
    def stationarity_test_conclusion(self, feature, returns = False):
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        results = self.stationarity_test(feature, returns = returns)
        for row_idx in range (results.shape[0]):
            test_name = results.index[row_idx]
            statistic = results.iat[row_idx, 0]
            if test_name == 'ADF Test':
                print (test_name)
                if statistic < results.iat[row_idx, 2]:
                    print("Estacionaria con un 99% de confianza")
                elif statistic < results.iat[row_idx, 3]:
                    print("Estacionaria con un 95% de confianza")
                elif statistic < results.iat[row_idx, 4]:
                    print("Estacionaria con un 90% de confianza")
                else:
                    print("No es estacionaria")
            elif test_name == 'KPSS Test':
                print (test_name)
                if statistic > results.iat[row_idx, 2]:
                    print("No estacionaria con un 99% de confianza")
                elif statistic > results.iat[row_idx, 3]:
                    print("No estacionaria con un 95% de confianza")
                elif statistic > results.iat[row_idx, 4]:
                    print("No estacionaria con un 90% de confianza")
                else:
                    print("Es estacionaria")
    def rolling_volatility(self, feature, window=20, returns=True, plot_original=False, peaks=False, threshold_factor=2, backend='matplotlib'):

        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
        rolling_volatility = time_series.rolling(window=window).std()
    
        if backend == 'matplotlib':

            plt.figure(figsize=(12, 6), facecolor='black')
            if peaks:
                threshold = rolling_volatility.mean() + threshold_factor * rolling_volatility.std()
                peaks_values = rolling_volatility[rolling_volatility > threshold]
                plt.scatter(peaks_values.index, peaks_values, color='red', marker='o', label='Picos de Volatilidad')
                plt.axhline(threshold, color='yellow', linestyle='--', label=f'Umbral ({threshold_factor}x Desv. Est.)')
                plt.title(f'Picos de Volatilidad en {feature_name}', color='white')
            if plot_original:
                plt.plot(time_series, color='yellow', alpha=0.6, label=f'Serie Original ({feature_name})')
            plt.plot(rolling_volatility, color='cyan', label=f'Volatilidad ({window}-ventana)')
            plt.title(f'Volatilidad en Ventanas Móviles ({feature_name})', color='white')
            plt.xlabel('Tiempo', color='white')
            plt.ylabel('Volatilidad', color='white')
            plt.grid(True, color='gray', linestyle='--')
            plt.tick_params(axis='x', colors='white')
            plt.tick_params(axis='y', colors='white')
            plt.gca().set_facecolor('black')
            plt.legend()
            plt.tight_layout()
            plt.show()
    
        elif backend == 'plotly':
            fig = go.Figure()
    
            if plot_original:
                fig.add_trace(go.Scatter(
                    x=time_series.index, 
                    y=time_series, 
                    mode='lines', 
                    name=f'Serie Original ({feature_name})', 
                    line=dict(color='yellow'), 
                    opacity=0.6 
                ))
    
            fig.add_trace(go.Scatter(
                x=rolling_volatility.index, 
                y=rolling_volatility, 
                mode='lines', 
                name=f'Volatilidad ({window}-ventana)', 
                line=dict(color='cyan')
            ))
    
            if peaks:
                threshold = rolling_volatility.mean() + threshold_factor * rolling_volatility.std()
                peaks_values = rolling_volatility[rolling_volatility > threshold]
                fig.add_trace(go.Scatter(
                    x=peaks_values.index, 
                    y=peaks_values, 
                    mode='markers', 
                    name='Picos de Volatilidad', 
                    marker=dict(color='red', symbol='circle')
                ))
                fig.add_hline(
                    y=threshold, 
                    line=dict(color='yellow', dash='dash'), 
                    annotation_text=f'Umbral ({threshold_factor}x Desv. Est.)', 
                    annotation_position='top right'
                )

            fig.update_layout(
                title=f'Volatilidad en Ventanas Móviles ({feature_name})',
                xaxis_title='Tiempo',
                yaxis_title='Volatilidad',
                template='plotly_dark',
                width=1200,
                height=600,  
                hovermode='x unified'  
            )
            fig.show()
        else:
            raise ValueError("El parámetro 'backend' debe ser 'matplotlib' o 'plotly'.")

    def _adfuller_(self, time_series):
        adf_result = adfuller(time_series, autolag='AIC')
        adf_output = {
            'ADF Statistic': adf_result[0],
            'p-value': adf_result[1],
            'Critical Values': adf_result[4]
        }
        return adf_output
    def _kpss_ (self, time_series):
        kpss_result = kpss(time_series, regression='c')
        kpss_output = {
            'KPSS Statistic': kpss_result[0],
            'p-value': kpss_result[1],
            'Critical Values': kpss_result[3]
        }
        return kpss_output
    def _read_feature_ (self, df, feature):
        if type(feature) == str:
            time_series = df[feature]
            feature_name = feature
        elif type(feature) == int:
            time_series = df.iloc[:, feature]
            feature_name = df.columns[feature]
        return time_series, feature_name
    def _clean_stat_result_ (self, test_results):
        data = {
            'Test': ['ADF Test', 'KPSS Test'],
            'Statistic': [test_results['ADF Test']['ADF Statistic'], test_results['KPSS Test']['KPSS Statistic']],
            'p-value': [test_results['ADF Test']['p-value'], test_results['KPSS Test']['p-value']],
            'Critical Value 1%': [test_results['ADF Test']['Critical Values']['1%'], test_results['KPSS Test']['Critical Values']['1%']],
            'Critical Value 5%': [test_results['ADF Test']['Critical Values']['5%'], test_results['KPSS Test']['Critical Values']['5%']],
            'Critical Value 10%': [test_results['ADF Test']['Critical Values']['10%'], test_results['KPSS Test']['Critical Values']['10%']]
        }
        df = pd.DataFrame(data)
        df.set_index('Test', inplace = True)
        return df

    def calculate_var(self, feature, confidence_level=0.95, method='parametric', returns = True):
        """
        Calcula el Value at Risk (VaR) para la serie temporal especificada.
        
        Parámetros:
        - feature: Nombre o índice de la columna en el DataFrame.
        - confidence_level: Nivel de confianza para el VaR (default=0.95).
        - method: Método para calcular el VaR ('parametric' o 'historical').
        
        Devuelve: El VaR calculado.
        """
        df = self.returns_df if returns else self.df
        time_series, feature_name = self._read_feature_(df, feature)
    
        if method == 'parametric':
            # VaR Paramétrico: Supone distribución normal de los retornos
            mean_return = time_series.mean()
            std_dev = time_series.std()
            z_score = np.abs(np.percentile(time_series, (1 - confidence_level) * 100))
            var = z_score * std_dev - mean_return
        elif method == 'historical':
            # VaR Histórico: Basado en el percentil de los retornos históricos
            var = np.percentile(time_series, (1 - confidence_level) * 100)
        else:
            raise ValueError("El método debe ser 'parametric' o 'historical'.")
    
        return var

class ROCCalculator(BaseEstimator, TransformerMixin):
    """
    Calculadora de la tasa de cambio (Rate of Change, ROC) para series temporales.

    Esta clase implementa un transformador que calcula el ROC o la derivada discreta de series temporales,
    con soporte para modos de transformación de 'returns' y 'log_returns'. También proporciona la capacidad
    de invertir la transformación.

    Parámetros:
    -----------
    fit_mode : str, opcional
        Modo en el cual se eligen las series temporales a transformar. Puede ser 'stationate' para seleccionar
        series no estacionarias o 'all_positive' para seleccionar series con valores siempre positivos.
        Por defecto es 'all_positive'.
    transform_mode : str, opcional
        Modo en el cual se calculan los retornos. Puede ser 'returns' (cálculo estándar de retornos) o
        'log_returns' (retornos logarítmicos). Por defecto es 'returns'.
    exception : bool, opcional
        Si es True, para series que no cumplen las condiciones de transformación tras el fit, se calcula la
        derivada discreta. Si es False, los valores de las series no transformadas permanecen sin cambios.
        Por defecto es True.
    period : int, opcional
        Período para calcular la transformación (cuántos periodos se desplazan las diferencias). Por defecto es 1.
    stationarity_threshold : float, opcional
        Valor p umbral para la prueba de estacionariedad (ADF). Si el valor p es mayor que este umbral,
        la serie es considerada no estacionaria. Por defecto es 0.05.
    """

    def __init__(self, fit_mode='all_positive', transform_mode='returns', exception=True, period=1, stationarity_threshold=0.05):
        valid_fit_modes = ['stationate', 'all_positive']
        valid_transform_modes = ['returns', 'log_returns']
        # Validación de los modos seleccionados
        if fit_mode not in valid_fit_modes:
            raise ValueError(f"'{fit_mode}' is not a valid mode. Choose from {valid_fit_modes}.")
        if transform_mode not in valid_transform_modes:
            raise ValueError(f"'{transform_mode}' is not a valid mode. Choose from {valid_transform_modes}.")

        # Inicialización de los atributos
        self.period = period
        self.fit_mode = fit_mode
        self.stationarity_threshold = stationarity_threshold
        self.transform_mode = transform_mode
        self.exception = exception

    def fit(self, X, y=None):
        """
        Ajusta el transformador a los datos, determinando qué series serán transformadas
        en función del `fit_mode` especificado.

        Parámetros:
        -----------
        X : pd.DataFrame
            DataFrame de entrada con series temporales.
        y : None, opcional
            Parámetro opcional para mantener compatibilidad con scikit-learn.

        Retorna:
        --------
        self : ROCCalculator
            Retorna la instancia del transformador ajustado.
        """
        self.columns = X.columns
        self.index = X.index
        X = X.values
        self.conditions = {}

        # Determina las condiciones para cada característica (serie temporal)
        if self.fit_mode == 'stationate':
            # Verifica la estacionariedad de cada serie
            for feature in range(X.shape[1]):
                values = X[:, feature]
                evaluation = self._check_stationarity_(values)
                self.conditions[feature] = evaluation
            self.deleted_values = X[:self.period, :].copy()
        elif self.fit_mode == 'all_positive':
            # Verifica que los valores de la serie sean siempre positivos
            for feature in range(X.shape[1]):
                values = X[:, feature]
                evaluation = self._check_for_non_positive_(values)
                self.conditions[feature] = evaluation
            self.deleted_values = X[:self.period, :].copy()

        return self

    def transform(self, X, y=None):
        """
        Aplica la transformación ROC o derivada discreta a los datos.

        Parámetros:
        -----------
        X : pd.DataFrame
            DataFrame de entrada con series temporales a transformar.
        y : None, opcional
            Parámetro opcional para mantener compatibilidad con scikit-learn.

        Retorna:
        --------
        pd.DataFrame
            DataFrame con las series transformadas.
        """
        X = X.values
        transformed_values = []

        # Realiza la transformación en función de las condiciones establecidas durante el fit
        for feature, condition in self.conditions.items():
            if condition:
                # Aplica la tasa de cambio
                transformed_values.append(np.expand_dims(self._roc_(X[:, feature]), axis=1))
            else:
                # Aplica la derivada discreta o deja la serie sin cambios según el valor de exception
                if self.exception:
                    transformed_values.append(np.expand_dims(self._discrete_derivative_(X[:, feature]), axis=1))
                else:
                    transformed_values.append(np.expand_dims(X[:, feature], axis=1))

        # Concatenación de los resultados transformados
        transformed_X = np.concatenate(transformed_values, axis=1)
        return pd.DataFrame(transformed_X[1:, :], columns=self._transform_column_names_(), index=self.index[1:])

    def inverse_transform(self, X, y=None):
        """
        Invierte la transformación aplicada a los datos.

        Parámetros:
        -----------
        X : pd.DataFrame
            DataFrame con las series transformadas.
        y : None, opcional
            Parámetro opcional para mantener compatibilidad con scikit-learn.

        Retorna:
        --------
        pd.DataFrame
            DataFrame con las series originales recuperadas.
        """
        X = X.values
        transformed_values = []

        # Invierte la transformación para cada característica
        for feature, condition in self.conditions.items():
            values = X[:, feature]
            full_values = np.concatenate([self.deleted_values[:, feature], values], axis=0)
            if condition:
                transformed_values.append(np.expand_dims(self._iroc_(full_values), axis=1))
            else:
                transformed_values.append(np.expand_dims(self._inverse_derivative_(full_values), axis=1))

        # Concatenación de los valores invertidos
        transformed_X = np.concatenate(transformed_values, axis=1)
        return pd.DataFrame(transformed_X, columns=self.columns, index=self.index)

    def _check_stationarity_(self, values):
        """
        Verifica si una serie es estacionaria utilizando la prueba de Dickey-Fuller aumentada (ADF).

        Parámetros:
        -----------
        values : array-like
            Serie de valores a evaluar.

        Retorna:
        --------
        bool
            True si la serie es no estacionaria, False si es estacionaria.
        """
        adf_test = adfuller(values)
        return adf_test[1] > self.stationarity_threshold

    def _check_for_non_positive_(self, values):
        """
        Verifica si todos los valores en la serie son positivos.

        Parámetros:
        -----------
        values : array-like
            Serie de valores a evaluar.

        Retorna:
        --------
        bool
            True si todos los valores son positivos, False en caso contrario.
        """
        return all(x > 0 for x in values)

    def _roc_(self, values):
        """
        Calcula la tasa de cambio o los retornos logarítmicos de una serie.

        Parámetros:
        -----------
        values : array-like
            Serie de valores para calcular la tasa de cambio.

        Retorna:
        --------
        array
            Serie transformada.
        """
        if self.transform_mode == 'returns':
            transformed_values = (values[self.period:] - values[:-self.period]) / values[:-self.period]
        elif self.transform_mode == 'log_returns':
            transformed_values = np.log(values[self.period:] / values[:-self.period])
        transformed_values = np.concatenate((np.full(self.period, np.nan), transformed_values))
        return transformed_values

    def _discrete_derivative_(self, values):
        """
        Calcula la derivada discreta de una serie.

        Parámetros:
        -----------
        values : array-like
            Serie de valores para calcular la derivada.

        Retorna:
        --------
        array
            Serie transformada.
        """
        transformed_values = (values[self.period:] - values[:-self.period]) / self.period
        transformed_values = np.concatenate((np.full(self.period, np.nan), transformed_values))
        return transformed_values

    def _inverse_derivative_(self, full_values):
        """
        Recupera la serie original a partir de la derivada discreta.

        Parámetros:
        -----------
        full_values : array-like
            Serie con la derivada discreta y los valores iniciales.

        Retorna:
        --------
        array
            Serie original recuperada.
        """
        initial_values = full_values[:self.period]
        transformed_values = np.cumsum(full_values[self.period:], axis=0) + initial_values[-1]
        recovered_values = np.concatenate([initial_values, transformed_values], axis=0)
        return recovered_values

    def _iroc_(self, full_values):
        """
        Invierte la transformación de la tasa de cambio.

        Parámetros:
        -----------
        full_values : array-like
            Serie con los valores transformados y los valores iniciales.

        Retorna:
        --------
        array
            Serie original recuperada.
        """
        if self.transform_mode == 'returns':
            return self._inverse_return_(full_values)
        elif self.transform_mode == 'log_returns':
            return self._inverse_log_return_(full_values)

    def _inverse_return_(self, full_values):
        """
        Recupera la serie original a partir de los retornos.

        Parámetros:
        -----------
        full_values : array-like
            Serie con los retornos y los valores iniciales.

        Retorna:
        --------
        array
            Serie original recuperada.
        """
        initial_values = full_values[:self.period]
        transformed_values = full_values[self.period:]
        full_recovered_values = np.concatenate([initial_values, np.cumprod(transformed_values + 1) * initial_values[-1]], axis=0)
        return full_recovered_values

    def _inverse_log_return_(self, full_values):
        """
        Recupera la serie original a partir de los retornos logarítmicos.

        Parámetros:
        -----------
        full_values : array-like
            Serie con los retornos logarítmicos y los valores iniciales.

        Retorna:
        --------
        array
            Serie original recuperada.
        """
        transformed_values = np.exp(np.cumsum(full_values[self.period:], axis=0) + np.log(full_values[self.period - 1]))
        full_recovered_values = np.concatenate([full_values[:self.period], transformed_values], axis=0)
        return full_recovered_values

    def _transform_column_names_(self):
        """
        Genera los nombres de las columnas transformadas.

        Retorna:
        --------
        list
            Lista de nombres de las columnas transformadas.
        """
        transformed_columns = []
        for feature_idx, condition in self.conditions.items():
            if condition:
                transformed_columns.append(self.columns[feature_idx] + '_' + self.transform_mode)
            else:
                if self.exception:
                    transformed_columns.append(self.columns[feature_idx] + '_diff')
                else:
                    transformed_columns.append(self.columns[feature_idx])
        return transformed_columns

class Returns_Calculator(BaseEstimator, TransformerMixin, StationarityTester):
    """
    Esta clase calcula los retornos porcentuales de un conjunto de características, dependiendo de si las 
    características pasan la prueba de estacionariedad.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.
    StationarityTester : Clase personalizada que contiene una función para evaluar la estacionariedad.

    Atributos:
    ----------
    threshold : float
        Umbral para determinar si una característica es estacionaria.
    
    period : int
        Período para el cálculo de los retornos porcentuales (n períodos previos).

    Métodos:
    --------
    __init__(threshold, period):
        Inicializa la clase con un umbral para la estacionariedad y un período para calcular los retornos.
    
    fit(X, y=None):
        Evalúa la estacionariedad de las características en X, almacena las columnas y los índices, 
        y calcula los valores eliminados para la inversa.
    
    transform(X, y=None):
        Aplica el cálculo de retornos a las características que no son estacionarias.
    
    inverse_transform(X, y=None):
        Restaura los valores originales, deshaciendo la transformación de los retornos porcentuales.
    """

    def __init__(self, threshold, period):
        """
        Inicializa la clase Returns_Calculator con el umbral para la estacionariedad y el período para los retornos.

        Parámetros:
        -----------
        threshold : float
            El umbral para determinar si una característica es estacionaria.
        
        period : int
            El período que se utilizará para calcular los retornos porcentuales.
        """
        self.threshold = threshold
        self.period = period

    def fit(self, X, y=None):
        """
        Ajusta el transformador evaluando la estacionariedad de cada característica y almacena información
        sobre las columnas e índices de los datos.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre las cuales se evaluará la estacionariedad.

        y : None
            No utilizado.

        Retorna:
        --------
        self : Returns_Calculator
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        self.index = X.index
        self.evaluations = {}
        for feature in X:
            evaluation = self.evaluate(X[feature])
            self.evaluations[feature] = evaluation
        self.deleted_values = X.iloc[:self.period, :].copy()
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos aplicando el cálculo de retornos a las características no estacionarias.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre el cual se aplicará la transformación.

        y : None
            No utilizado.

        Retorna:
        --------
        transformed_X : DataFrame
            Los datos transformados, sin las primeras 'period' filas.
        """
        transformed_X = X.copy()
        for feature, condition in self.evaluations.items():
            if condition:
                transformed_X[feature] = transformed_X[feature].pct_change(periods=self.period)
        transformed_X = transformed_X.iloc[self.period:, :]
        return transformed_X

    def inverse_transform(self, X, y=None):
        """
        Deshace la transformación de los retornos porcentuales, restaurando los valores originales.

        Parámetros:
        -----------
        X : DataFrame
            Los datos transformados de los cuales se quieren recuperar los valores originales.

        y : None
            No utilizado.

        Retorna:
        --------
        restored_df : DataFrame
            Los datos restaurados a su forma original antes de la transformación.
        """
        restored_df = pd.concat([self.deleted_values, X], axis=0)
        restored_df.columns = self.columns
        restored_df.index = self.index
        for idx in range(restored_df.shape[1]):
            if not self.evaluations[self.columns[idx]]:
                continue
            unstructured_values = restored_df.iloc[:, idx].values
            reestructured_values = []
            for value_idx, current_value in enumerate(unstructured_values):
                if value_idx < self.period:
                    reestructured_values.append(current_value)
                else:
                    reestructured_values.append(reestructured_values[value_idx - self.period] * (1 + unstructured_values[value_idx]))
            restored_df.iloc[:, idx] = reestructured_values
        return restored_df


class Stationater(BaseEstimator, TransformerMixin, StationarityTester):
    """
    Esta clase aplica diferencias a las características para convertirlas en estacionarias, 
    hasta un límite máximo de diferenciación.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.
    StationarityTester : Clase personalizada que contiene una función para evaluar la estacionariedad.

    Atributos:
    ----------
    threshold : float
        Umbral para determinar si una característica es estacionaria.
    
    diff_limit : int
        Límite máximo de diferenciaciones permitidas para lograr estacionariedad.

    Métodos:
    --------
    __init__(threshold, diff_limit):
        Inicializa la clase con el umbral para la estacionariedad y el límite máximo de diferenciaciones.
    
    fit(X, y=None):
        Evalúa la estacionariedad de las características y calcula el número de diferenciaciones necesarias para cada una.
    
    transform(X, y=None):
        Aplica las diferenciaciones necesarias a las características para hacerlas estacionarias.
    
    inverse_transform(X, y=None):
        Deshace las diferenciaciones aplicadas, restaurando los valores originales.
    """

    def __init__(self, threshold, diff_limit):
        """
        Inicializa la clase Stationater con un umbral para la estacionariedad y un límite de diferenciación.

        Parámetros:
        -----------
        threshold : float
            El umbral para determinar si una característica es estacionaria.
        
        diff_limit : int
            El límite máximo de diferenciaciones permitidas para una característica.
        """
        self.threshold = threshold
        self.diff_limit = diff_limit

    def fit(self, X, y=None):
        """
        Ajusta el transformador evaluando la estacionariedad de cada característica y determina cuántas 
        diferenciaciones se necesitan para cada una.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre las cuales se evaluará la estacionariedad.

        y : None
            No utilizado.

        Retorna:
        --------
        self : Stationater
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        self.index = X.index
        self.orders_diff = {}
        for feature in range(X.shape[1]):
            feature_diff_orders = 0
            X_for_test = X.copy()
            contador = 0
            while True:
                evaluation = self.evaluate(X_for_test.iloc[:, feature])
                if not evaluation:
                    break
                if contador == self.diff_limit:
                    print(f'diff limit reached by {feature}')
                    break
                feature_diff_orders += 1
                X_for_test = pd.DataFrame(np.diff(X_for_test, axis=0))
                contador += 1
            self.orders_diff[feature] = feature_diff_orders
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos aplicando diferenciaciones a las características que no son estacionarias.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre el cual se aplicará la transformación.

        y : None
            No utilizado.

        Retorna:
        --------
        new_df : DataFrame
            Los datos transformados con diferenciaciones aplicadas para hacerlos estacionarios.
        """
        new_columns = []
        self.deleted_values = {}
        for feature, order_diff in self.orders_diff.items():
            feature_deleted_values = []
            new_column = X.iloc[:, feature].values
            if order_diff == 0:
                new_columns.append(new_column)
            else:
                for order in range(order_diff):
                    feature_deleted_values.append(new_column[0])
                    new_column = np.diff(new_column)
                new_columns.append(new_column)
            self.deleted_values[feature] = feature_deleted_values

        largest_shape = max(len(arr) for arr in new_columns)
        for feature, array in enumerate(new_columns):
            if array.dtype == 'int64':
                array = array.astype('float64')
            while array.shape[0] != largest_shape:
                array = np.insert(array, 0, np.nan)
            new_columns[feature] = array

        new_df = pd.DataFrame(new_columns).T
        new_df.columns = self.columns

        for idx in range(new_df.shape[0]):
            row = new_df.iloc[idx, :]
            if row.isna().any():
                for feature in range(new_df.shape[1]):
                    if not pd.isna(row.iloc[feature]):
                        self.deleted_values[feature].append(row.iloc[feature])

        new_df = new_df.dropna()
        new_df.set_index(self.index[max(self.orders_diff.values()):], inplace=True)
        return new_df

    def inverse_transform(self, X, y=None):
        """
        Deshace las diferenciaciones aplicadas, restaurando los valores originales.

        Parámetros:
        -----------
        X : DataFrame
            Los datos transformados de los cuales se quieren recuperar los valores originales.

        y : None
            No utilizado.

        Retorna:
        --------
        reconstructed_df : DataFrame
            Los datos restaurados a su forma original antes de la transformación.
        """
        reconstructed_df = pd.DataFrame(columns=self.columns)
        for feature, order in self.orders_diff.items():
            series = X.iloc[:, feature]
            if order == 0:
                for current_order in range(max(self.orders_diff.values())):
                    series = np.insert(series, 0, self.deleted_values[feature][current_order])
            else:
                for current_order in range(max(self.orders_diff.values())):
                    series = np.cumsum(np.insert(series, 0, self.deleted_values[feature][current_order]))
            reconstructed_df[self.columns[feature]] = series
        return reconstructed_df


class WindowedTransformer(BaseEstimator, TransformerMixin):
    """
    Clase para dividir un DataFrame en dos arrays de ventanas de datos, uno de predictores y otro de etiquetas, 
    basándose en el número de timesteps (n_past y n_future). Este transformador es útil para tareas de predicción de series de tiempo 
    donde se requiere dividir el dataset en ventanas de observaciones pasadas y futuras.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    n_past : int
        Número de pasos de tiempo pasados a usar como predictores.
    
    n_future : int
        Número de pasos de tiempo futuros a usar como etiquetas.

    Métodos:
    --------
    __init__(n_past, n_future):
        Inicializa la clase con los timesteps para predictores y etiquetas.
    
    fit(X, y=None):
        Guarda los nombres de las columnas del DataFrame para su posterior uso.
    
    transform(X_input, y=None):
        Genera dos arrays: uno con las ventanas de datos pasados (predictores) y otro con los futuros (etiquetas).
    
    inverse_transform(Xt, y=None):
        Reconstruye un DataFrame a partir de los arrays de ventanas de predictores y etiquetas.
    """

    def __init__(self, n_past, n_future):
        """
        Inicializa la clase WindowedTransformer con el número de timesteps para los predictores y etiquetas.

        Parámetros:
        -----------
        n_past : int
            El número de pasos de tiempo pasados que se utilizarán como predictores.
        
        n_future : int
            El número de pasos de tiempo futuros que se utilizarán como etiquetas.
        """
        self.n_past = n_past
        self.n_future = n_future

    def fit(self, X, y=None):
        """
        Ajusta el transformador almacenando los nombres de las columnas del DataFrame para su posterior uso.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos de entrada con características temporales.
        
        y : None
            No utilizado.

        Retorna:
        --------
        self : WindowedTransformer
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        #self.index = X.index
        return self
        
    def transform(self, X_input, y=None):
        """
        Divide el DataFrame en ventanas de datos. El resultado es una tupla de dos arrays: uno con las ventanas de
        los datos pasados (predictores) y otro con las ventanas de los datos futuros (etiquetas).

        Parámetros:
        -----------
        X_input : pd.DataFrame
            El conjunto de datos de entrada con características temporales.

        y : None
            No utilizado.

        Retorna:
        --------
        tuple : (np.array, np.array)
            - El primer array contiene las ventanas de los datos pasados (predictores).
            - El segundo array contiene las ventanas de los datos futuros (etiquetas), con forma ajustada según las características.
        """
        if (X_input.shape[0] <= self.n_past):
            print ('Input shape not big enough for given n_past')
            return None, None
        elif (X_input.shape[0] <= self.n_future):
            print ('Input shape not big enough for given n_future')
            return None, None
        X = []
        Ys = []
        for i in range(self.n_past, len(np.array(X_input)) + 1 - self.n_future):
            X.append(np.array(X_input)[i - self.n_past : i, 0 : np.array(X_input).shape[1]])
        
        for layer in range(np.array(X_input).shape[1]):
            Y = []
            for i in range(self.n_past, len(np.array(X_input)) + 1 - self.n_future):
                Y.append(np.array(X_input)[i : i + self.n_future, layer])
            Ys.append(np.array(Y))

        X, Ys = np.array(X), np.array(Ys)
        Ys = Ys.transpose(1, 2, 0)
        return (X, Ys)

    def inverse_transform(self, Xt, y=None):
        """
        Reconstruye un DataFrame a partir de dos arrays de ventanas de predictores y etiquetas.
        Combina las ventanas pasadas y futuras para crear una secuencia de datos continua.

        Parámetros:
        -----------
        Xt : tuple
            Una tupla que contiene:
            - El primer array con las ventanas de predictores.
            - El segundo array con las ventanas de etiquetas.
        
        y : None
            No utilizado.

        Retorna:
        --------
        itransformed_df : pd.DataFrame
            El DataFrame reconstruido a partir de las ventanas de predictores y etiquetas.
        """
        X, Ys = Xt
        itransformed_df = pd.DataFrame()

        for layer in range(X.shape[2]):
            itransformed_df[layer] = np.concatenate(
                (np.concatenate((X[0, :, layer], Ys[0, :, layer])), Ys[1:, -1, layer])
            )
        itransformed_df.columns = self.columns
        #itransformed_df.index = self.index
        return itransformed_df


class StandardScalerAdapter(BaseEstimator, TransformerMixin):
    """
    Adaptador personalizado para aplicar la estandarización a cada columna
    de un DataFrame de forma independiente utilizando `StandardScaler` de scikit-learn.

    Esta clase permite aplicar transformaciones de estandarización (media 0 y desviación estándar 1)
    a cada columna de un DataFrame. Es útil para mantener las propiedades de cada característica
    individual, especialmente cuando se trabaja con DataFrames que tienen múltiples columnas.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    columns : pd.Index
        Almacena los nombres de las columnas del DataFrame para ser reutilizadas en las transformaciones.
    
    scalers : dict
        Diccionario que almacena un objeto `StandardScaler` de scikit-learn para cada columna del DataFrame.

    Métodos:
    --------
    fit(X, y=None):
        Ajusta un `StandardScaler` para cada columna del DataFrame.
    
    transform(X, y=None):
        Aplica la estandarización a cada columna utilizando los escaladores ajustados.
    
    inverse_transform(X, y=None):
        Revierte la estandarización, devolviendo los datos a sus valores originales.
    """

    def fit(self, X, y=None):
        """
        Ajusta un `StandardScaler` para cada columna del DataFrame. 
        Se almacena un escalador para cada columna para su posterior uso en la transformación.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame cuyas columnas se van a estandarizar.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        self : StandardScalerAdapter
            El propio objeto ajustado, necesario para el patrón de scikit-learn fit/transform.
        """
        self.columns = X.columns
        #self.index = X.index
        self.scalers = {}
        for column in range(X.values.shape[1]):
            scaler = StandardScaler()
            scaler.fit(X.values[:, column].reshape(-1, 1))
            self.scalers[column] = scaler
        
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos estandarizando cada columna utilizando los escaladores previamente ajustados.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame que se va a transformar.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        pd.DataFrame : DataFrame transformado con las mismas columnas originales,
        pero con los valores estandarizados (media 0 y desviación estándar 1).
        """
        transformed_X = X.values.copy()
        for column in range(X.values.shape[1]):
            transformed_X[:, column] = self.scalers[column].transform(X.values[:, column].reshape(-1, 1)).flatten()
        return pd.DataFrame(transformed_X, columns=self.columns)

    def inverse_transform(self, X, y=None):
        """
        Deshace la transformación (escalado) y devuelve los valores a su escala original.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame transformado que se quiere revertir a sus valores originales.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        pd.DataFrame : DataFrame con los valores originales desescalados.
        """
        itransformed_X = X.values.copy()
        for column in range(X.values.shape[1]):
            itransformed_X[:, column] = self.scalers[column].inverse_transform(X.values[:, column].reshape(-1, 1)).flatten()
        return pd.DataFrame(itransformed_X, columns=self.columns)#, index=self.index)


class StationatersEnsemble(BaseEstimator, TransformerMixin):
    """
    Clase para aplicar múltiples "estacionadores" secuencialmente sobre un DataFrame.
    Esto es útil cuando, al intentar estacionar series temporales, algunas de las series pueden necesitar
    más de un proceso de diferenciación para volverse estacionarias.

    El objetivo es empaquetar varios estacionadores y aplicar un conjunto de transformaciones
    para asegurar que todas las series en el DataFrame se vuelvan estacionarias.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    threshold : float
        Umbral de significancia para determinar si una serie temporal es estacionaria.
    
    diff_limit : int
        Límite máximo de diferenciaciones que puede aplicar cada estacionador individual a una serie temporal.
    
    stationaters_limit : int
        Límite máximo de estacionadores que pueden ser aplicados secuencialmente.

    Métodos:
    --------
    __init__(threshold, diff_limit, stationaters_limit):
        Inicializa la clase con el umbral de significancia, el límite de diferenciaciones y el límite de estacionadores.
    
    fit(X, y=None):
        Ajusta múltiples estacionadores secuenciales al DataFrame para asegurar que todas las series sean estacionarias.
    
    transform(X, y=None):
        Aplica las transformaciones de los estacionadores ajustados al DataFrame para hacerlo estacionario.
    
    inverse_transform(X, y=None):
        Revierte las transformaciones aplicadas por los estacionadores, restaurando el DataFrame a su forma original.
    """

    def __init__(self, threshold, diff_limit, stationaters_limit):
        """
        Inicializa la clase StationatersEnsemble con el umbral de significancia para la estacionariedad, el límite
        de diferenciación para cada estacionador y el límite máximo de estacionadores.

        Parámetros:
        -----------
        threshold : float
            El umbral de significancia para evaluar la estacionariedad de las series temporales.
        
        diff_limit : int
            El límite máximo de diferenciaciones que se permite aplicar a cada serie temporal por estacionador.
        
        stationaters_limit : int
            El límite máximo de estacionadores que pueden ser aplicados de forma secuencial.
        """
        self.threshold = threshold
        self.diff_limit = diff_limit
        self.stationaters_limit = stationaters_limit

    def fit(self, X, y=None):
        """
        Ajusta múltiples estacionadores secuenciales al DataFrame. Para cada columna (serie temporal) del DataFrame,
        se aplica un proceso de diferenciación (estacionador) hasta que todas las series sean estacionarias o hasta
        que se alcance el límite de estacionadores.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos de entrada con características temporales.
        
        y : None
            No utilizado.

        Retorna:
        --------
        self : StationatersEnsemble
            El propio objeto ajustado, necesario para el patrón de scikit-learn fit/transform.
        """
        evaluator = StationarityTester(threshold=self.threshold)
        self.stationaters = {}
        evaluations = [evaluator.evaluate(X[feature]) for feature in X]

        current_stationated_X = X.copy()
        order = 0
        while any(evaluations):
            if order == self.stationaters_limit:
                print('Stationaters limit reached')
                break
            current_stationater = Stationater(threshold=self.threshold, diff_limit=self.diff_limit)
            current_stationated_X = current_stationater.fit_transform(current_stationated_X)
            self.stationaters[order] = current_stationater
            evaluations = [evaluator.evaluate(current_stationated_X[feature]) for feature in X]
            order += 1
        return self

    def transform(self, X, y=None):
        """
        Aplica las transformaciones de los estacionadores ajustados al DataFrame.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos a transformar.

        y : None
            No utilizado.

        Retorna:
        --------
        pd.DataFrame : El DataFrame transformado con las series temporales estacionarias.
        """
        if len(self.stationaters) == 0:
            return X

        current_stationated_X = X.copy()
        for stationater in self.stationaters.values():
            current_stationated_X = stationater.transform(current_stationated_X)
        
        return current_stationated_X

    def inverse_transform(self, X, y=None):
        """
        Revierte las transformaciones aplicadas por los estacionadores, devolviendo el DataFrame a su forma original.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos transformados que se desea revertir.

        y : None
            No utilizado.

        Retorna:
        --------
        pd.DataFrame : El DataFrame restaurado con las series temporales en su forma original.
        """
        current_inverse_transformed_X = X.copy()
        
        if len(self.stationaters) == 0:
            return X

        for stationater in reversed(self.stationaters.values()):
            current_inverse_transformed_X = stationater.inverse_transform(current_inverse_transformed_X)
        
        return current_inverse_transformed_X

def split_simple(df, porcentaje_separacion_train, porcentaje_separacion_val):
    """
    Divide el DataFrame en conjuntos de entrenamiento, validación y prueba de manera temporal simple.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        porcentaje_separacion_train (float): Porcentaje de datos que se utilizarán para entrenamiento (entre 0 y 1).
        porcentaje_separacion_val (float): Porcentaje de datos que se utilizarán para validación (entre 0 y 1).
    Returns:
        tuple: Conjunto de entrenamiento, conjunto de validación y conjunto de prueba.
    """
    q1 = int(len(df) * porcentaje_separacion_train)
    q2 = int(len(df) * (porcentaje_separacion_train + porcentaje_separacion_val))
    
    train = df.iloc[:q1].copy()
    val = df.iloc[q1:q2].copy()
    test = df.iloc[q2:].copy()
    
    return train, val, test

def split_time_series_cv(df, n_splits):
    """
    Realiza una validación cruzada para series temporales, dividiendo los datos en n_splits pliegues.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        n_splits (int): Número de pliegues para la validación cruzada.
        
    Returns:
        list of tuple: Lista de pares (entrenamiento, prueba) para cada pliegue.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    splits = []
    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index].copy(), df.iloc[test_index].copy()
        splits.append((train, test))
    return splits
    
def split_sliding_window(df, train_size, test_size, step_size):
    """
    Divide el DataFrame utilizando una ventana deslizante para entrenamiento y prueba.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        train_size (int): Tamaño de la ventana de entrenamiento.
        test_size (int): Tamaño de la ventana de prueba.
        step_size (int): Número de pasos para mover la ventana.
        
    Returns:
        list of tuple: Lista de pares (entrenamiento, prueba) para cada ventana.
    """
    splits = []
    for start in range(0, len(df) - train_size - test_size + 1, step_size):
        train = df.iloc[start:start + train_size].copy()
        test = df.iloc[start + train_size:start + train_size + test_size].copy()
        splits.append((train, test))
    return splits
