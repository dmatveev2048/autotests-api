from concurrent import futures  # Импорт пула потоков для асинхронного выполнения
import grpc  # Импорт библиотеки gRPC

# Импортируем сгенерированные файлы
import course_service_pb2
import course_service_pb2_grpc

# 1. Реализация логики сервиса
# Наследуемся СТРОГО от course_service_pb2_grpc.CourseServiceServicer
class CourseServiceServicer(course_service_pb2_grpc.CourseServiceServicer):

    # Метод обязательно принимает request (данные) и context (метаданные)
    def GetCourse(self, request, context):
        print(f"Получен запрос GetCourse для course_id: {request.course_id}")

        # Возвращаем объект ответа с данными из задания
        return course_service_pb2.GetCourseResponse(
            course_id=request.course_id, # Берем из запроса
            title="Автотесты API",        # Константа по заданию
            description="Будем изучать написание API автотестов" # Константа по заданию
        )

# 2. Настройка и запуск сервера
def serve():
    # Создаем сервер с использованием пула потоков (до 10 потоков)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Регистрируем наш сервис на сервере
    # Используем функцию add_CourseServiceServicer_to_server из сгенерированного файла
    course_service_pb2_grpc.add_CourseServiceServicer_to_server(
        CourseServiceServicer(), server
    )

    # Настраиваем прослушивание порта 50051
    server.add_insecure_port('[::]:50051')

    # Запускаем сервер
    server.start()
    print("gRPC сервер запущен на порту 50051...")

    # Ожидаем завершения работы сервера (чтобы процесс не закрылся сразу)
    server.wait_for_termination()

# Запуск скрипта
if __name__ == "__main__":
    serve()