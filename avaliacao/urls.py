from django.urls import path

from avaliacao import views

urlpatterns = [
    path(
        'avaliacoes_desempenho/listar/',
        views.AvaliacaoDesempenhoListarView.as_view(),
        name='avaliacao-listar',
    ),
    path(
        'avaliacoes_desempenho/cadastrar/',
        views.AvaliacaoDesempenhoCadastrarView.as_view(),
        name='avaliacao-cadastrar',
    ),
    path(
        'avaliacoes_desempenho/cadastrar_avaliacao_form/',
        views.AvaliacaoDesempenhoFormView.as_view(),
        name='avaliacao-form',
    ),
    path(
        'avaliacoes_desempenho/<int:id_avaliacao>/visualizar/',
        views.AvaliacaoDesempenhoVisualizarView.as_view(),
        name='avaliacao-visualizar',
    ),
    path(
        'avaliacoes_desempenho/<int:id_avaliacao>/iniciar/',
        views.AvaliacaoDesempenhoIniciarView.as_view(),
        name='avaliacao-iniciar',
    ),
    path(
        'avaliacoes_desempenho/<int:id_avaliacao>/editar/',
        views.AvaliacaoDesempenhoEditarView.as_view(),
        name='avaliacao-editar',
    ),
    path(
        'avaliacoes_desempenho/<int:id_avaliacao>/dar_feedback/',
        views.AvaliacaoDesempenhoDarFeedbackView.as_view(),
        name='avaliacao-dar-feedback',
    ),
    path(
        'avaliacoes_desempenho/<int:id_avaliacao>/concluir/',
        views.AvaliacaoDesempenhoConcluirView.as_view(),
        name='avaliacao-concluir',
    ),
    path(
        'tipo_item_avaliacao_desempenho/',
        views.TipoItemAvaliacaoDesempenhoListView.as_view(),
        name='tipo-item-list',
    ),
    path(
        'tipo_item_avaliacao_desempenho/<int:pk>/',
        views.TipoItemAvaliacaoDesempenhoDetailView.as_view(),
        name='tipo-item-detail',
    ),
]