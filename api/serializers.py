from rest_framework import serializers
from .models import CustomUser,Job,Application ,Contact

class RegisterUserSerializer(serializers.ModelSerializer):  #this is for sending and receiving data! 
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password","first_name","last_name"]  #the obligatory fields to be registered
        extra_kwargs = {"password": {"write_only": True}}  # thats why here we set that the password is only to be accepted , not be sent again when we want to give info about the user


    def create(self, validated_data):  #the serializer will make sure that the data is validated , by matching the model and the inputs received  fields = ["id", "username", "password"] , if it matches he will
        print(validated_data)           #pass the validated_data
        user = CustomUser.objects.create_user(**validated_data)
        #addedotp
        user.is_active = False  # Deactivate account until it is confirmed
        user.generate_code()  #functions called from the user model
        user.send_confirmation_email()
        return user 
    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

'''class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']  # Only allow updates to these fields
        read_only_fields = ('email',)  # Email should not be editable

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance'''

""" def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance """



class JobSerializer(serializers.ModelSerializer):
    total_applications = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = "__all__"     






class ApplicationSerializer(serializers.ModelSerializer):
    # Without job_details: The app retrieves a list of applications, each with a job ID
    #we save the job_details (job.title) to display it in the application same for candidate details
    job_details = serializers.ReadOnlyField(source='job.title') #these are just for ez reference instead of doing job.title , we say job_details directly
    candidate_details = serializers.ReadOnlyField(source='candidate.email')
   #job_id = serializers.ReadOnlyField(source='job.id') 
    

    class Meta:
        model = Application
        fields = ['id', 'cv', 'cover_letter', 'status', 'job_details', 'candidate_details','created_at','candidate','job' ]  #here we put the data that will be passed in and out , we cant access job nor post it for example if we dont put it here
        read_only_fields = ['job_details', 'candidate_details','candidate','job']  # Ensure these fields are read-only

    def validate_cv(self, value):
        """
        Add custom validation for the CV upload.
        For example, checking the file size.
        """
        max_file_size = 1024 * 1024 * 5  # 5 MB
        if value.size > max_file_size:
            raise serializers.ValidationError("The CV file is too large. Maximum size allowed is 5MB.")
        return value



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


