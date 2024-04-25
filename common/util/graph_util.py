import plotly.graph_objects as go
import pandas as pd

def draw_bars_by_csv(df, num_rows, x_name="keyphrarse", y_name="similarity"): #when convert csv df to graph
    fig = go.Figure()
    for i in range(num_rows):
        fig.add_trace(
            go.Bar(
                x=eval(df[x_name][i]),
                y=eval(df[y_name][i]),
                name=f"{i}번째 행"
            )
        )
    fig.update_yaxes(range=[0.0, 0.8])
    fig.show()
    fig.write_html('draws_bars_by_csv.html', auto_open=True)

def draw_bars_by_list(num_rows, x, y): #when convert 2-dimlist to graph
    fig = go.Figure()
    for i in range(num_rows):       
        fig.add_trace(
            go.Bar(
                x=x[i],
                y=y[i],
                name=f"{i}번째 행"
            )
        )
    fig.update_yaxes(range=[0.0, 0.8])
    fig.show()
    # fig.write_html('draws_bars_by_list.html', auto_open=True)


# def main():
#     df= pd.read_excel("./../dataset/inv/KR/김민수_all.xlsx")
#     df=df.sort_values(by=["출원일"],axis=0)
#     print(df)
#
# if __name__ == "__main__":
#     main()
