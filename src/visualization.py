import shap
import matplotlib.pyplot as plt

def plot_shap_waterfall(model, df_encoded, st):
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df_encoded)

        if isinstance(shap_values, list):
            shap_vals = shap_values[1][0]
            expected_val = explainer.expected_value[1]
        else:
            shap_vals = shap_values[0]
            expected_val = explainer.expected_value

        shap.initjs()
        fig = plt.figure(figsize=(10, 4))
        shap.plots._waterfall.waterfall_legacy(
            expected_val,
            shap_vals,
            df_encoded.iloc[0],
            max_display=10,
            show=False
        )
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"⚠️ SHAP waterfall plot failed: {e}")
