from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from avaliacao.models import (
    AvaliacaoDesempenho,
    Colaborador,
    StatusAvaliacao,
    TipoItemAvaliacaoDesempenho,
)
from avaliacao.serializers import (
    AvaliacaoDesempenhoDetalheSerializer,
    AvaliacaoDesempenhoFormSerializer,
    AvaliacaoDesempenhoListSerializer,
    CadastrarAvaliacaoSerializer,
    EditarAvaliacaoSerializer,
    TipoItemAvaliacaoDesempenhoSerializer,
)


class AvaliacaoDesempenhoListarView(APIView):
    def get(self, request):
        avaliacoes = AvaliacaoDesempenho.objects.select_related(
            'colaborador', 'supervisor'
        ).all()
        serializer = AvaliacaoDesempenhoListSerializer(avaliacoes, many=True)
        return Response(serializer.data)


class AvaliacaoDesempenhoFormView(APIView):
    def get(self, request):
        colaboradores = Colaborador.objects.all()
        supervisores = Colaborador.objects.all()
        data = {
            'colaboradores': colaboradores,
            'supervisores': supervisores,
        }
        from avaliacao.serializers import ColaboradorSerializer
        serializer = AvaliacaoDesempenhoFormSerializer({
            'colaboradores': colaboradores,
            'supervisores': supervisores,
        })
        return Response(serializer.data)


class AvaliacaoDesempenhoVisualizarView(APIView):
    def get(self, request, id_avaliacao):
        avaliacao = get_object_or_404(
            AvaliacaoDesempenho.objects.select_related(
                'colaborador', 'supervisor'
            ).prefetch_related('itens__tipo_item_avaliacao_desempenho'),
            pk=id_avaliacao,
        )
        serializer = AvaliacaoDesempenhoDetalheSerializer(avaliacao)
        return Response(serializer.data)


class AvaliacaoDesempenhoIniciarView(APIView):
    def post(self, request, id_avaliacao):
        avaliacao = get_object_or_404(AvaliacaoDesempenho, pk=id_avaliacao)
        if avaliacao.status_avaliacao != StatusAvaliacao.CRIADA:
            return Response(
                {'erro': 'Apenas avaliações com status "Criada" podem ser iniciadas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avaliacao.iniciar()
        serializer = AvaliacaoDesempenhoDetalheSerializer(avaliacao)
        return Response(serializer.data)


class AvaliacaoDesempenhoEditarView(APIView):
    def post(self, request, id_avaliacao):
        avaliacao = get_object_or_404(AvaliacaoDesempenho, pk=id_avaliacao)
        if avaliacao.status_avaliacao not in [
            StatusAvaliacao.EM_ELABORACAO,
            StatusAvaliacao.EM_AVALIACAO,
        ]:
            return Response(
                {'erro': 'Apenas avaliações "Em elaboração" ou "Em avaliação" podem ser editadas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = EditarAvaliacaoSerializer(
            avaliacao, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        avaliacao = serializer.save()
        return Response(AvaliacaoDesempenhoDetalheSerializer(avaliacao).data)


class AvaliacaoDesempenhoDarFeedbackView(APIView):
    def post(self, request, id_avaliacao):
        avaliacao = get_object_or_404(AvaliacaoDesempenho, pk=id_avaliacao)
        if avaliacao.status_avaliacao != StatusAvaliacao.EM_ELABORACAO:
            return Response(
                {'erro': 'Apenas avaliações "Em elaboração" podem receber feedback.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avaliacao.dar_feedback()
        serializer = AvaliacaoDesempenhoDetalheSerializer(avaliacao)
        return Response(serializer.data)


class AvaliacaoDesempenhoConcluirView(APIView):
    def post(self, request, id_avaliacao):
        avaliacao = get_object_or_404(AvaliacaoDesempenho, pk=id_avaliacao)
        if avaliacao.status_avaliacao != StatusAvaliacao.EM_AVALIACAO:
            return Response(
                {'erro': 'Apenas avaliações "Em avaliação" podem ser concluídas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avaliacao.concluir()
        serializer = AvaliacaoDesempenhoDetalheSerializer(avaliacao)
        return Response(serializer.data)


class AvaliacaoDesempenhoCadastrarView(APIView):
    def post(self, request):
        serializer = CadastrarAvaliacaoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'erro': 'Campos obrigatórios ausentes'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avaliacao = serializer.save()
        return Response(
            'Avaliação cadastrada com sucesso!',
            status=status.HTTP_201_CREATED,
        )


class TipoItemAvaliacaoDesempenhoListView(APIView):
    def get(self, request):
        tipos = TipoItemAvaliacaoDesempenho.objects.all()
        serializer = TipoItemAvaliacaoDesempenhoSerializer(tipos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TipoItemAvaliacaoDesempenhoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TipoItemAvaliacaoDesempenhoDetailView(APIView):
    def get(self, request, pk):
        tipo = get_object_or_404(TipoItemAvaliacaoDesempenho, pk=pk)
        serializer = TipoItemAvaliacaoDesempenhoSerializer(tipo)
        return Response(serializer.data)

    def post(self, request, pk):
        tipo = get_object_or_404(TipoItemAvaliacaoDesempenho, pk=pk)
        serializer = TipoItemAvaliacaoDesempenhoSerializer(
            tipo, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)