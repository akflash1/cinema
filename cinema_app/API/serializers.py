from rest_framework import serializers
from cinema_app.models import User, Hall, Film, Session, Purchase


class UserRegistrationSerializer(serializers.ModelSerializer):
    total_spent = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'total_spent']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ('id', 'name', 'size',)

    def validate_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Name must be greater than 0.')
        return value

    def validate_size(self, value):
        if value <= 0:
            raise serializers.ValidationError('Size must be greater than 0.')
        return value


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'name', 'description', 'date_start', 'date_finish',)

    def validate(self, attrs):
        date_start = attrs.get('date_start')
        date_finish = attrs.get('date_finish')

        if date_start and date_finish and date_start > date_finish:
            raise serializers.ValidationError('Start date must be less than end date.')

        return attrs

    def validate_name(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('Name should be longer.')
        return value

    def validate_description(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('Description should be longer.')
        return value


class SessionSerializer(serializers.ModelSerializer):
    rest_of_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Session
        fields = ('id', 'date', 'time_start', 'time_end', 'price', 'rest_of_seats', 'hall', 'film',)

    def validate(self, attrs):
        time_start = attrs.get('time_start')
        time_end = attrs.get('time_end')
        hall = attrs.get('hall')
        attrs['rest_of_seats'] = hall.size

        if time_start and time_end and time_start > time_end:
            raise serializers.ValidationError('Start time must be less than end time.')

        if time_start and time_end and hall:
            conflicting_sessions = Session.objects.filter(
                hall=hall,
                time_start__lt=time_end,
                time_end__gt=time_start
            )

            if self.instance:
                conflicting_sessions = conflicting_sessions.exclude(pk=self.instance.pk)

            if conflicting_sessions.exists():
                raise serializers.ValidationError('This session conflicts with an existing session.')
        return attrs

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0.')
        return value


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'amount', 'ticket', 'buyer',)

    def validate(self, attrs):
        amount = attrs.get('amount')
        ticket = attrs.get('ticket')

        if amount <= 0:
            raise serializers.ValidationError('Amount must be greater than 0.')

        if amount > ticket.rest_of_seats:
            raise serializers.ValidationError('Rest of seats must be greater than amount.')
        return attrs
