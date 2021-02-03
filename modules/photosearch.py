import random
from testcanarybot import objects

class Main(objects.libraryModule):
    @objects.priority(commands = ["картинка"])
    async def photo_search(self, tools, package):
        response = await tools.api.photos.search(
            type = "service", 
            q = " ".join(package.items[1:-1])
            )
            
        results, count = [
            "photo{owner_id}_{id}".format(owner_id = i.owner_id, id = i.id) for i in response.items
        ], response.count
        
        await tools.api.messages.send(
            random_id = tools.random_id(),
            peer_id = package.peer_id,
            message = f"Вот ваша коллекция фотографий [5/{count}]",
            attachment = ",".join(sorted(results, key=lambda results: random.random())[:5]),
        )


