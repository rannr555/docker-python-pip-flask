import threading

class Wallet:
    def __init__(self, default_resource = 0):
        self.resources = {'pennies' : default_resource}

    def get(self, resource):
        return self.resources.get(resource, 0)

    def change(self, resource, delta):
        # This function MUST BLOCK until the wallet has enough resources to satisfy the request.
        self.resources[resource] = self.resources.get(resource, 0)
        self.resources[resource] += delta
        return self.resources[resource]


    def try_change(self, resource, delta):
        # Like change, but if change would block this method instead leaves the resource unchanged and returns False.        
        self.resources[resource] = self.resources.get(resource, 0)
        self.resources[resource] += delta
        return self.resources[resource]


    def transaction(self, **delta):
        """
        Like calling change(key, value) for each key:value in `delta`, except:
        - All changes are made at once. If any change would block, the entire transaction blocks.
            Only continues once *all* the changes can be made as one atomic action.
        """ 
        return_dict = {}
        for key, value in delta.items():
            self.resources[key] += value
            return_dict[key] = self.resources[key]

        return return_dict