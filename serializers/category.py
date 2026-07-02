from rest_framework import serializers


class CategoryTreeSerializer(serializers.Serializer):
    def to_representation(self, roots):
        result = {}
        for root in roots:
            children = root.get_children()
            result[root.name] = {child.name : child.id for child in children}

        return result