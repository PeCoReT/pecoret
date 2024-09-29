from djangoql.schema import DjangoQLSchema as DjQLSchema


class DjangoQLSchema(DjQLSchema):
    def excluded(self, model):
        # use lazy imports for including/excluding models based on label names
        return model in self.exclude or (self.include and self.model_label(model) not in self.include)
