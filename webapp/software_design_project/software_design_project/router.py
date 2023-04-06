from software_design.viewsets import StudentViewset
from software_design.viewsets import StaffViewset, Mac_pointViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('student', StudentViewset)
router.register('staff', StaffViewset)
router.register('mac_point', Mac_pointViewset)

# localhost:p/api/student/5
# GET, POST, UPDATE, DELETE
# list, re
