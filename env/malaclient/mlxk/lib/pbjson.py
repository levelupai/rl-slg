import json
from google.protobuf.descriptor import FieldDescriptor as FD

class ConvertException(Exception):
    pass

def dict2pb(cls, adict, strict=False):
    """
    Takes a class representing the ProtoBuf Message and fills it with data from
    the dict.
    """
    obj = cls()
    for field in obj.DESCRIPTOR.fields:
        if not field.label == field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if not field.name in adict:
            raise ConvertException('Field "%s" missing from descriptor dictionary.'
                                   % field.name)
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise ConvertException(
                    'Key "%s" can not be mapped to field in %s class.'
                    % (key, type(obj)))
    for field in obj.DESCRIPTOR.fields:
        if not field.name in adict:
            continue
        msg_type = field.message_type
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                for sub_dict in adict[field.name]:
                    item = getattr(obj, field.name).add()
                    item.CopyFrom(dict2pb(msg_type._concrete_class, sub_dict))
            else:
                map(getattr(obj, field.name).append, adict[field.name])
        else:
            if field.type == FD.TYPE_MESSAGE:
                value = dict2pb(msg_type._concrete_class, adict[field.name])
                getattr(obj, field.name).CopyFrom(value)
            else:
                setattr(obj, field.name, adict[field.name])
    return obj


def pb2dict(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a dict.
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field in obj.DESCRIPTOR.fields:
        # if not getattr(obj, field.name):
        #     continue
        if not field.label == FD.LABEL_REPEATED:
            if not field.type == FD.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                if value:
                    adict[field.name] = value
        else:
            if field.type == FD.TYPE_MESSAGE:
                adict[field.name] = \
                    [pb2dict(v) for v in getattr(obj, field.name)]
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


def json2pb(cls, json, strict=False):
    """
    Takes a class representing the Protobuf Message and fills it with data from
    the json string.
    """
    return dict2pb(cls, json.loads(json), strict)


def pb2json(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a json string.
    """
    return json.dumps(pb2dict(obj), sort_keys=True, indent=4)
