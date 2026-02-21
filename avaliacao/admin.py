from django.contrib import admin

from avaliacao.models import (
    AvaliacaoDesempenho,
    Colaborador,
    ItemAvaliacaoDesempenho,
    TipoItemAvaliacaoDesempenho,
)


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(TipoItemAvaliacaoDesempenho)
class TipoItemAvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    list_display = ['id', 'dimensao', 'tipo_item_avaliacao_desempenho', 'descricao']
    list_filter = ['dimensao']
    search_fields = ['tipo_item_avaliacao_desempenho', 'descricao']


class ItemAvaliacaoDesempenhoInline(admin.TabularInline):
    model = ItemAvaliacaoDesempenho
    extra = 0
    fields = ['tipo_item_avaliacao_desempenho', 'nota', 'observacoes']
    readonly_fields = []


@admin.register(AvaliacaoDesempenho)
class AvaliacaoDesempenhoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'colaborador',
        'supervisor',
        'mes_competencia',
        'status_avaliacao',
        'nota',
    ]
    list_filter = ['status_avaliacao', 'mes_competencia']
    search_fields = ['colaborador__nome', 'supervisor__nome']
    readonly_fields = ['nota']
    date_hierarchy = 'mes_competencia'
    inlines = [ItemAvaliacaoDesempenhoInline]
    actions = ['action_iniciar', 'action_dar_feedback', 'action_concluir']

    @admin.action(description='Iniciar avaliações selecionadas')
    def action_iniciar(self, request, queryset):
        for avaliacao in queryset.filter(status_avaliacao='Criada'):
            avaliacao.iniciar()

    @admin.action(description='Dar feedback nas avaliações selecionadas')
    def action_dar_feedback(self, request, queryset):
        for avaliacao in queryset.filter(status_avaliacao='Em elaboração'):
            avaliacao.dar_feedback()

    @admin.action(description='Concluir avaliações selecionadas')
    def action_concluir(self, request, queryset):
        for avaliacao in queryset.filter(status_avaliacao='Em avaliação'):
            avaliacao.concluir()