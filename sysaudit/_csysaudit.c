#include "Python.h"

struct CsysauditState {
  PyObject* hooks;
};

#define csysaudit_state(o) ((struct CsysauditState*)PyModule_GetState(o))


static PyObject* csysaudit_audit(PyObject* self, PyObject* const *args, Py_ssize_t argc) {
  if (argc == 0) {
    PyErr_SetString(PyExc_TypeError, "audit() missing 1 required positional argument: 'event'");
    return NULL;
  }

  PyObject* return_value = NULL;
  PyObject* event_name = NULL;
  PyTupleObject* event_args = NULL;
  PyObject* hooks = NULL;
  PyObject* hook = NULL;

  event_name = args[0];
  if (!event_name) {
    PyErr_SetString(PyExc_TypeError, "expected str for argument 'event'");
    goto exit;
  }

  if (!PyUnicode_Check(event_name)) {
    PyErr_Format(PyExc_TypeError, "expected str for argument 'event', not %.200s",
                 Py_TYPE(event_name)->tp_name);
    goto exit;
  }

  event_args = (PyTupleObject*)PyTuple_New(argc - 1);
  if (!event_args) {
    goto exit;
  }

  PyObject** dst = event_args->ob_item;
  for (Py_ssize_t i = 1; i < argc; i++) {
    PyObject* item = args[i];
    Py_INCREF(item);
    dst[i - 1] = item;
  }

  hooks = PyObject_GetIter(csysaudit_state(self)->hooks);
  if (!hooks) {
    goto exit;
  }

  while ((hook = PyIter_Next(hooks)) != NULL) {
    PyObject *o;
    o = PyObject_CallFunctionObjArgs(hook, event_name, event_args, NULL);
    if (!o) {
      break;
    }
    Py_DECREF(o);
    Py_CLEAR(hook);
  }

  Py_INCREF(Py_None);
  return_value = Py_None;

 exit:
  Py_XDECREF(hook);
  Py_XDECREF(hooks);
  Py_XDECREF(event_args);

  return return_value;
};


static PyObject* csysaudit_addaudithook(PyObject* self, PyObject* const *args, Py_ssize_t nargs, PyObject* kwnames) {
  PyObject* hook;

  if (nargs == 0) {
    PyErr_SetString(PyExc_TypeError, "addaudithook() missing 1 required positional argument: 'hook'");
    return NULL;
  }

  hook = args[0];

  if (PyList_Append(csysaudit_state(self)->hooks, hook) < 0) {
    return NULL;
  }

  Py_RETURN_NONE;
};

static PyMethodDef csysaudit_methods[] = {
                                          {"audit",           (PyCFunction)(void(*)(void))csysaudit_audit, METH_FASTCALL, PyDoc_STR("") },
                                          {"addaudithook",    (PyCFunction)(void(*)(void))csysaudit_addaudithook, METH_FASTCALL, PyDoc_STR("") },
                                          { NULL, NULL }
};

PyDoc_VAR(csysaudit_doc) = PyDoc_STR("");

static struct PyModuleDef csysaudit = {
                                       PyModuleDef_HEAD_INIT,
                                       "sysaudit.csysaudit",
                                       csysaudit_doc,
                                       sizeof(struct CsysauditState),
                                       csysaudit_methods,
                                       NULL,
                                       NULL,
                                       NULL,
                                       NULL
};


PyObject* PyInit_csysaudit() {
  PyObject* res = PyModule_Create(&csysaudit);
  if (!res) return NULL;

  csysaudit_state(res)->hooks = PyList_New(0);

  return res;
};
