from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'rank',
            'privilege',
            'tg_link',
            'vk_link',
            'discord_link',
            'steam_link',
            'github_link',
            'market_privilege',
            'buy_privilege',
            'scam',
        )
