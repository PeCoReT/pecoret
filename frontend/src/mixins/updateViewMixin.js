export const updateViewMixin = {
    methods: {
        clearObjectToPk(obj) {
            // if an object has a primary key, return it, otherwise return object.
            // helper for model choice fields
            if (typeof obj === 'object' && obj.pk) {
                return obj.pk
            }
            return obj;
        },
        isManyObject(manyObj, data) {
            if (typeof manyObj === 'object' && manyObj.length > 0 && manyObj[0].pk) {
                return true;
            }
            return false;
        }
    }
}