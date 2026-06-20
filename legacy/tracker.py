import time


class RequestTracker:
    def __init__(self):
        self.requests = []

    def track(
        self, request_name, func, input_tokens=0, output_tokens=0, *args, **kwargs
    ):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsedTime = end - start
        cost = self.calculate_cost(input_tokens, output_tokens)
        self.requests.append(
            {
                "name": request_name,
                "latency": elapsedTime,
                "cost": cost,
                "result": result,
            }
        )
        return result

    def report(self):
        for req in self.requests:
            print(
                f"Name: {req['name']}, Latency : {req['latency']:.2f}s, Cost : {req['cost']}"
            )

        latencies = [req["latency"] for req in self.requests]
        print(f"Ortalama: {sum(latencies)/len(latencies):.2f}s")

        total_cost = sum([req["cost"] for req in self.requests])
        print(f"Toplam Cost: ${total_cost:.6f}")

    def calculate_cost(self, input_tokens, output_tokens):
        input_cost = (input_tokens / 1_000_000) * 0.150
        output_cost = (output_tokens / 1_000_000) * 0.600

        return input_cost + output_cost
