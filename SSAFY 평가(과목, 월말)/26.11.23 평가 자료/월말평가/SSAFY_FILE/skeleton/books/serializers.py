from rest_framework import serializers
from .models import Book, Comment


# 도서 목록 조회용 serializer
class BookListSerializer(serializers.ModelSerializer):
    num_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        # 1. 목록 조회 시 각 도서의 id, title, author, num_of_comments만 응답되도록 수정
        # fields = '__all__'
        fields = ('id', 'title', 'author', 'num_of_comments',)

    def get_num_of_comments(self, obj):
        return Comment.objects.count()


# 도서 생성 / 수정용 serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# 도서 상세 조회용 serializer (댓글 목록 포함)
class BookDetailSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)

    comments = CommentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


# 댓글 serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    