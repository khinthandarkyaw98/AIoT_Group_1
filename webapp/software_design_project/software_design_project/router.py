from software_design.viewsets import StudentViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('student', StudentViewset)

# localhost:p/api/student/5
# GET, POST, UPDATE, DELETE
# list, retrieve