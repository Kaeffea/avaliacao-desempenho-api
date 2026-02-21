from rest_framework import serializers

from avaliacao.models import (
    AvaliacaoDesempenho,
    Colaborador,
    ItemAvaliacaoDesempenho,
    TipoItemAvaliacaoDesempenho,
)


class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['id_colaborador', 'nome']

    id_colaborador = serializers.IntegerField(source='id', read_only=True)


class TipoItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoItemAvaliacaoDesempenho
        fields = ['id', 'dimensao', 'tipo_item_avaliacao_desempenho', 'descricao']


class ItemAvaliacaoDesempenhoSerializer(serializers.ModelSerializer):
    tipo_item_avaliacao_desempenho = TipoItemAvaliacaoDesempenhoSerializer(read_only=True)

    class Meta:
        model = ItemAvaliacaoDesempenho
        fields = ['id', 'tipo_item_avaliacao_desempenho', 'nota', 'observacoes']


class ItemAvaliacaoDesempenhoEditarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAvaliacaoDesempenho
        fields = ['id', 'nota', 'observacoes']


class StatusSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    descricao = serializers.CharField(source='status_avaliacao')

    def get_id(self, obj):
        status_map = {
            'Criada': 1,
            'Em elaboração': 2,
            'Em avaliação': 3,
            'Concluída': 4,
        }
        return status_map.get(obj.status_avaliacao, 0)


class AvaliacaoDesempenhoListSerializer(serializers.ModelSerializer):
    id_avaliacao = serializers.IntegerField(source='id', read_only=True)
    nome_colaborador = serializers.CharField(source='colaborador.nome', read_only=True)
    competencia = serializers.SerializerMethodField()
    status = StatusSerializer(source='*')

    class Meta:
        model = AvaliacaoDesempenho
        fields = ['id_avaliacao', 'nome_colaborador', 'competencia', 'status']

    def get_competencia(self, obj):
        return obj.mes_competencia.strftime('%m/%Y')


class AvaliacaoDesempenhoDetalheSerializer(serializers.ModelSerializer):
    id_avaliacao = serializers.IntegerField(source='id', read_only=True)
    id_colaborador = serializers.IntegerField(source='colaborador.id', read_only=True)
    nome_colaborador = serializers.CharField(source='colaborador.nome', read_only=True)
    id_supervisor = serializers.IntegerField(source='supervisor.id', read_only=True)
    nome_supervisor = serializers.CharField(source='supervisor.nome', read_only=True)
    competencia = serializers.SerializerMethodField()
    status = StatusSerializer(source='*')
    itens = ItemAvaliacaoDesempenhoSerializer(many=True, read_only=True)

    class Meta:
        model = AvaliacaoDesempenho
        fields = [
            'id_avaliacao',
            'id_colaborador',
            'nome_colaborador',
            'id_supervisor',
            'nome_supervisor',
            'competencia',
            'status',
            'nota',
            'sugestoes_supervisor',
            'observacoes_avaliado',
            'itens',
        ]

    def get_competencia(self, obj):
        return obj.mes_competencia.strftime('%m/%Y')


class AvaliacaoDesempenhoFormSerializer(serializers.Serializer):
    colaboradores = ColaboradorSerializer(many=True)
    supervisores = ColaboradorSerializer(many=True)


class CadastrarAvaliacaoSerializer(serializers.ModelSerializer):
    competencia = serializers.CharField(write_only=True)

    class Meta:
        model = AvaliacaoDesempenho
        fields = ['id_colaborador', 'id_supervisor', 'competencia']

    id_colaborador = serializers.IntegerField(write_only=True)
    id_supervisor = serializers.IntegerField(write_only=True)

    def validate_competencia(self, value):
        try:
            from datetime import datetime
            datetime.strptime(f'01/{value}', '%d/%m/%Y')
        except ValueError:
            raise serializers.ValidationError(
                'Formato inválido. Use MM/AAAA.'
            )
        return value

    def create(self, validated_data):
        from datetime import datetime
        competencia_str = validated_data.pop('competencia')
        id_colaborador = validated_data.pop('id_colaborador')
        id_supervisor = validated_data.pop('id_supervisor')
        mes_competencia = datetime.strptime(
            f'01/{competencia_str}', '%d/%m/%Y'
        ).date()
        colaborador = Colaborador.objects.get(pk=id_colaborador)
        supervisor = Colaborador.objects.get(pk=id_supervisor)
        avaliacao = AvaliacaoDesempenho.objects.create(
            colaborador=colaborador,
            supervisor=supervisor,
            mes_competencia=mes_competencia,
        )
        for tipo in TipoItemAvaliacaoDesempenho.objects.all():
            ItemAvaliacaoDesempenho.objects.create(
                avaliacao_desempenho=avaliacao,
                tipo_item_avaliacao_desempenho=tipo,
                nota=1,
            )
        return avaliacao


class EditarAvaliacaoSerializer(serializers.Serializer):
    sugestoes_supervisor = serializers.CharField(
        required=False, allow_blank=True, default=''
    )
    observacoes_avaliado = serializers.CharField(
        required=False, allow_blank=True, default=''
    )
    itens = ItemAvaliacaoDesempenhoEditarSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        instance.sugestoes_supervisor = validated_data.get(
            'sugestoes_supervisor', instance.sugestoes_supervisor
        )
        instance.observacoes_avaliado = validated_data.get(
            'observacoes_avaliado', instance.observacoes_avaliado
        )
        instance.save(update_fields=['sugestoes_supervisor', 'observacoes_avaliado'])

        itens_data = validated_data.get('itens', [])
        for item_data in itens_data:
            ItemAvaliacaoDesempenho.objects.filter(
                pk=item_data['id'],
                avaliacao_desempenho=instance,
            ).update(
                nota=item_data.get('nota'),
                observacoes=item_data.get('observacoes', ''),
            )

        instance.atualizar_nota()
        instance.refresh_from_db()
        return instance