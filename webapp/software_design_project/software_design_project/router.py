from software_design.viewsets import StudentViewset
from software_design.viewsets import StaffViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('student', StudentViewset)
router.register('staff', StaffViewset)

# localhost:p/api/student/5
# GET, POST, UPDATE, DELETE
# list, retrieve
