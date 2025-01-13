import cv2
from django.http import JsonResponse
from .action_handler import ActionHandler
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def start_camera(request):
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)
        action_handler = ActionHandler()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            action, coordinates = action_handler.process_frame(frame)
            if action:
                frame = action_handler.draw_result(frame, action, coordinates)

            cv2.imshow('Action Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return JsonResponse({"status": "camera closed"})
    return JsonResponse({"status": "method not allowed"}, status=405)

# Create your views here.
