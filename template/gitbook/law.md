# <i class="fa fa-balance-scale"></i> Loi N°{{ modified[current_law].law }}

## <i class="fa fa-pencil-square-o"></i> Articles modifiés

{%- for article in modified[current_law].articles %}
* [Article {{ article.id }}]({{ modified[current_law].law }}-{{ article.id }}.md)
{%- endfor %}