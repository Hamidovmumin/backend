from rest_framework import serializers


class CategoryTreeSerializer(serializers.Serializer):
    # def to_representation(self, roots):
    #     result = {}
    #     for root in roots:
    #         children = root.get_children()
    #         result[root.name] = {child.name : child.id for child in children}
    #
    #     return result

    def to_representation(self, instance):
        return [self.build_node(cat) for cat in instance]

    def build_node(self, cat):
        return {
            "id": cat.id,
            "name": cat.name,
            "slug": cat.slug,  # <-- əlavə et
            "children": [self.build_node(c) for c in cat.get_children()]
            if hasattr(cat, "get_children") else []
        }