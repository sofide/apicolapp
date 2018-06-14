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
        'body_table': [[st.date, st.hives, st.nucs] for st in status_history],
    }

    return table
