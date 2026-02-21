from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class DimensaoItemAvaliacao(models.TextChoices):
    COMPORTAMENTO = 'Comportamento', 'Comportamento'
    ENTREGAS = 'Entregas', 'Entregas'
    TRABALHO_EM_EQUIPE = 'Trabalho em equipe', 'Trabalho em equipe'


class StatusAvaliacao(models.TextChoices):
    CRIADA = 'Criada', 'Criada'
    EM_ELABORACAO = 'Em elaboração', 'Em elaboração'
    EM_AVALIACAO = 'Em avaliação', 'Em avaliação'
    CONCLUIDA = 'Concluída', 'Concluída'


class TipoItemAvaliacaoDesempenho(models.Model):
    dimensao = models.CharField(
        max_length=50,
        choices=DimensaoItemAvaliacao.choices,
        verbose_name='Dimensão',
    )
    tipo_item_avaliacao_desempenho = models.CharField(
        max_length=255,
        verbose_name='Tipo de item',
    )
    descricao = models.TextField(verbose_name='Descrição')

    class Meta:
        verbose_name = 'Tipo de Item de Avaliação'
        verbose_name_plural = 'Tipos de Item de Avaliação'
        ordering = ['dimensao', 'tipo_item_avaliacao_desempenho']

    def __str__(self):
        return f'{self.dimensao} — {self.tipo_item_avaliacao_desempenho}'


class Colaborador(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')

    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class AvaliacaoDesempenho(models.Model):
    colaborador = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='avaliacoes',
        verbose_name='Colaborador',
    )
    supervisor = models.ForeignKey(
        Colaborador,
        on_delete=models.PROTECT,
        related_name='avaliacoes_supervisionadas',
        verbose_name='Supervisor',
    )
    mes_competencia = models.DateField(verbose_name='Mês de competência')
    status_avaliacao = models.CharField(
        max_length=20,
        choices=StatusAvaliacao.choices,
        default=StatusAvaliacao.CRIADA,
        verbose_name='Status',
    )
    nota = models.FloatField(null=True, blank=True, default=0, verbose_name='Nota')
    sugestoes_supervisor = models.TextField(
        blank=True,
        default='',
        verbose_name='Sugestões do supervisor',
    )
    observacoes_avaliado = models.TextField(
        blank=True,
        default='',
        verbose_name='Observações do avaliado',
    )

    class Meta:
        verbose_name = 'Avaliação de Desempenho'
        verbose_name_plural = 'Avaliações de Desempenho'
        ordering = ['-mes_competencia']
        constraints = [
            models.UniqueConstraint(
                fields=['colaborador', 'mes_competencia'],
                name='unique_colaborador_mes_competencia',
            )
        ]

    def __str__(self):
        return (
            f'{self.colaborador} — '
            f'{self.mes_competencia.strftime("%m/%Y")}'
        )

    def atualizar_nota(self):
        itens = self.itens.all()
        total_tipos = TipoItemAvaliacaoDesempenho.objects.count()
        if total_tipos == 0:
            self.nota = 0
        else:
            soma = sum(item.nota for item in itens)
            self.nota = (soma / (total_tipos * 5)) * 100
        self.save(update_fields=['nota'])

    def iniciar(self):
        self.status_avaliacao = StatusAvaliacao.EM_ELABORACAO
        self.save(update_fields=['status_avaliacao'])

    def dar_feedback(self):
        self.status_avaliacao = StatusAvaliacao.EM_AVALIACAO
        self.save(update_fields=['status_avaliacao'])

    def concluir(self):
        self.status_avaliacao = StatusAvaliacao.CONCLUIDA
        self.save(update_fields=['status_avaliacao'])


class ItemAvaliacaoDesempenho(models.Model):
    avaliacao_desempenho = models.ForeignKey(
        AvaliacaoDesempenho,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Avaliação de desempenho',
    )
    tipo_item_avaliacao_desempenho = models.ForeignKey(
        TipoItemAvaliacaoDesempenho,
        on_delete=models.PROTECT,
        related_name='itens',
        verbose_name='Tipo de item',
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Nota',
    )
    observacoes = models.TextField(
        blank=True,
        default='',
        verbose_name='Observações',
    )

    class Meta:
        verbose_name = 'Item de Avaliação'
        verbose_name_plural = 'Itens de Avaliação'
        ordering = ['tipo_item_avaliacao_desempenho']

    def __str__(self):
        return (
            f'{self.avaliacao_desempenho} — '
            f'{self.tipo_item_avaliacao_desempenho}'
        )