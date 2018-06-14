from bokeh import plotting, embed

from apiary.models import Apiary, ApiaryStatus


def apiary_history_table(apiary):
    """
    Given an apiary it will return elements of a table with its ApiaryStatus data.

    Returns a dict with two keys:
        - 'headers':A list with the table headers in spanish = ['Fecha', 'Colmenas', 'Núcleos']

        - 'body':   A list of lists, representing an apiary table.
                    Each row will represent an ApiaryStatus related to the given Apiary object.
                    Data will be structured with the next format = [date, hives, nucs]
    """
    status_history = apiary.status_history.all()

    table = {
        'headers': ['Fecha', 'Colmenas', 'Núcleos'],
        'body': [[st.date, st.hives, st.nucs] for st in status_history if st.date != None],
    }

    return table


def apiary_history_chart(apiary_table, title=None):
    """
    Generates a lines chart representing an apiary's evolution. It will present two lines:
        - black = number of hives
        - orange = number of nucs

    Input:
        - a list of lists where each row has the follow structure: [date, hives, nucs]
        - (optional) a chart title

    Output: script and div components of a chart.
    """
    x_axis, hives, nucs = zip(*apiary_table)

    plot = plotting.figure(
        title=title,
        x_axis_label='Fecha',
        y_axis_label='Cantidad',
        x_axis_type='datetime',
    )
    plot.title.text_font_size = '1.5em'
    plot.title.align = 'center'

    plot.xaxis.axis_label_text_font_size = '1em'
    plot.yaxis.axis_label_text_font_size = '1em'

    plot.line(x_axis, hives, legend='Colmenas', line_width=2, line_color='black')
    plot.line(x_axis, nucs, legend='Núcleos', line_width=2, line_color='orange')

    return embed.components(plot)
