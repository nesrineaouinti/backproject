from django.shortcuts import render
from .models import CustomUser,Job,Application
from rest_framework import generics, status
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CheckIfAdminWithRecievedAccessTokenView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] #this will accept the access token sent from the front 
    # and now we will analyze it and extract if the user is admin

    def get(self, request):
        # request.user is automatically set by the JWTAuthentication
        user = request.user
        is_admin = user.is_staff or user.is_superuser
        return Response({"is_admin": is_admin})
    



def hello_view(request):
    return HttpResponse("Hello")

#JUST FOR TEST
class SendEmailAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        from_email = 'fstalert2023@gmail.com'  
        recipient_list = [request.data.get('to_email', '')]

        send_mail(subject, message, from_email, recipient_list)

        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)


class SendConfirmationCodeView(APIView):  #used for sending code when reset/change password and for resending code , for sending code when signup is automatically sent from the serializer
    permission_classes = [AllowAny]

    def post(self,request,email):
        
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_code()
            user.send_confirmation_email()
            return Response({'detail': 'Confirmation code resent successfully.'})
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User with this email does not exist or is already active.'}, status=status.HTTP_404_NOT_FOUND)



class VerifyCodeView(APIView):   #verify code for reset password /change password
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        print(email,code)
        try:
            user = CustomUser.objects.get(email=email, confirmation_code=code)
            
            return Response({'detail': 'Code verified successfully.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid email or code.'}, status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        print(new_password)
        if not email or not new_password:
            return Response({'detail': 'Email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=email) #is_active=true allow only registered users to resetpassword ,however sometimes user forgets his password before validating account with code
            user.set_password(new_password)  #set_password hashes the pw
            user.save()
            return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)






















#class based views
class RegisterUserView(generics.CreateAPIView):  #generics.CREATE it will create a new User for us, we give it the queryset , the serializer(having the model), and who can do it , and it will automatically prepare the creating process
    queryset = CustomUser.objects.all()             #the data to be searched in order to not create the same user twice
    serializer_class = RegisterUserSerializer           #what kind of data to be accepted to make a new user
    permission_classes = [AllowAny]                  #who can call this ? anyone even if someone is not authenticated , any geust on our website      

#addedotp
class ConfirmUserView(APIView):
    permission_classes = [AllowAny] #anyone can send his email and the code sent to him in order to confirm his account
    def post(self, request,email):  #include email in paramùeters or do this to extract the email from the url email = self.kwargs['email']
        code = request.data.get('code')
        
        try:
            user = CustomUser.objects.get(email=email, confirmation_code=code, is_active=False)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid confirmation code or email.'}, status=status.HTTP_400_BAD_REQUEST)

        
        user.is_active = True
        user.confirmation_code = None  # Clear the confirmation code
        user.save()

        return Response({'detail': 'User confirmed successfully.'},)
    

    

class UpdateUserView(generics.UpdateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Returns the user instance that matches the logged-in user
        return self.request.user

class GetUserView(generics.RetrieveAPIView):
    
    serializer_class = RegisterUserSerializer  
    def get_object(self):  #Override the get_object method to return the current user's data.
        return self.request.user    
    
'''class UpdateUsereView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()   #check on all the emails
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can update information

    def get_object(self):
        #  users are only able to update their own information
        return self.request.user'''
#one view/serizler for updating name+last name and one view/serial +otp verification in backend for updating pw or do email click verification (anyway should be managed in the backend becuz anyone can alter the front side)
    


'''class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):    #post : to handle POST request !! it receives as para the req we send
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

'''
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST) '''



class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  # Only admin users can create jobs
class JobListView(generics.ListAPIView):   #view Allll the jobs {kjfd,fojdfd;,ofd} {jkfd,fkdjfd,fdjfd } ...
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  
class JobDetailView(generics.RetrieveAPIView):   #view only one job , you just specify the id in urls.py
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  
class JobUpdateView(generics.UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  # Only admin users can update jobs

    
            
        
class JobDeleteView(generics.DestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]  # Only admin users can delete jobs



# class ApplicationCreateView(generics.CreateAPIView):   #set perm to isadmin !
#     serializer_class = ApplicationSerializer
#     #by default perm classes isAuthenticated for security , thats why u cant access api when u are not logged in unless u say allowAny
        
#     def perform_create(self, serializer):
#         job_id = self.request.data.get('job_id')  #!!! we should send the job_id from the frontend when creating an application
#         job = Job.objects.get(id=job_id)
#         serializer.save(candidate=self.request.user,job=job)
#         #we are embedding the whole job and the whole candidat (not just their ID) in the application table so it will be easier to access their info


class ApplicationCreateView(generics.CreateAPIView):   #set perm to isadmin !
    serializer_class = ApplicationSerializer
    #by default perm classes isAuthenticated for security , thats why u cant access api when u are not logged in unless u say allowAny
        
    def perform_create(self, serializer):
        job_id = self.kwargs['job_id']  # Get job_id from the URL parameter
        job = Job.objects.get(id=job_id)
        serializer.save(candidate=self.request.user,job=job)
        #we are embedding the whole job and the whole candidat (not just their ID) in the application table so it will be easier to access their info












class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    def get_queryset(self):
        """This view returns a list of all applications for an admin user,
        but only applications belonging to the currently authenticated user
        if they are not admin."""
        user = self.request.user
        if user.is_staff or user.is_superuser:  # Checks if the user is an admin
            return Application.objects.all()
        else:
            return Application.objects.filter(candidate=user)
        

        
        

class ApplicationsByJobView(generics.ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        """
        This view returns a list of all applications for a specific job ID.
        """
        job_id = self.kwargs['job_id']  # Get job_id from the URL parameter
        return Application.objects.filter(job__id=job_id)





class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer 
   # permission_classes = [IsAdminUser] #this is for the admin when he clicks on an application he can get details of the user
#update status here
#we dont need delete view , when the admin deletes the job , we specified on_delete=models.CASCADE, so the application will be deleted as well        

    def patch(self, request, *args, **kwargs):  #for update status 
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['accepted', 'rejected', 'in review']:
            application.status = new_status
            application.save()
            return Response({"status": "Application status updated to " + new_status}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)


'''class ApplicationActions extends React.Component {
  handleStatusChange = (newStatus) => {
    axios.patch(`/api/applications/${this.props.applicationId}/`, { status: newStatus })
      .then(response => {
        alert('Application status updated!');
        // Optionally update the state or perform other actions
      })
      .catch(error => {
        console.error('Error updating status:', error);
        alert('Failed to update status.');
      });
  };

  render() {
    return (
      <div>
        <button onClick={() => this.handleStatusChange('accepted')}>Accept</button>
        <button onClick={() => this.handleStatusChange('rejected')}>Reject</button>
      </div>
    );
  }
}

export default ApplicationActions; '''



class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class JobApplicationStatsView(APIView):

    def get(self, request):
        total_jobs = Job.objects.count()
        total_applications = Application.objects.count()
        total_rejected = Application.objects.filter(status='rejected').count()
        total_accepted = Application.objects.filter(status='accepted').count()
        total_sent = Application.objects.filter(status='sent').count()
        total_in_review = Application.objects.filter(status='in review').count()

        data = {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'total_rejected': total_rejected,
            'total_accepted': total_accepted,
            'total_sent': total_sent,
            'total_in_review': total_in_review,
        }

        return Response(data)